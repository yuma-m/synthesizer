import numpy as np
import pytest
import scipy.signal

from synthesizer import Filter, FilterType, Synthesizer, Waveform

RATE = 16000


def _sine(frequency, length=1.0, rate=RATE):
    return np.sin(2.0 * np.pi * frequency * np.arange(int(rate * length)) / rate)


def _gain(filter_, frequency):
    """RMS gain of steady-state response to a sine wave"""
    wave = _sine(frequency)
    filtered = filter_.apply(wave)
    # skip the transient at the beginning
    return np.sqrt(np.mean(filtered[RATE // 2 :] ** 2) / np.mean(wave[RATE // 2 :] ** 2))


def test_lowpass():
    filter_ = Filter(FilterType.lowpass, cutoff=1000.0, rate=RATE)
    assert _gain(filter_, 100.0) == pytest.approx(1.0, abs=0.01)
    assert _gain(filter_, 1000.0) == pytest.approx(1.0 / np.sqrt(2.0), abs=0.01)
    assert _gain(filter_, 5000.0) < 0.05


def test_highpass():
    filter_ = Filter(FilterType.highpass, cutoff=1000.0, rate=RATE)
    assert _gain(filter_, 100.0) < 0.02
    assert _gain(filter_, 1000.0) == pytest.approx(1.0 / np.sqrt(2.0), abs=0.01)
    assert _gain(filter_, 5000.0) == pytest.approx(1.0, abs=0.05)


def test_bandpass():
    filter_ = Filter(FilterType.bandpass, cutoff=1000.0, resonance=5.0, rate=RATE)
    assert _gain(filter_, 1000.0) == pytest.approx(1.0, abs=0.01)
    assert _gain(filter_, 300.0) < 0.1
    assert _gain(filter_, 3000.0) < 0.1


def test_resonance_boosts_cutoff():
    flat = Filter(FilterType.lowpass, cutoff=1000.0, resonance=0.707, rate=RATE)
    resonant = Filter(FilterType.lowpass, cutoff=1000.0, resonance=4.0, rate=RATE)
    assert _gain(resonant, 1000.0) == pytest.approx(4.0, rel=0.02)
    assert _gain(resonant, 1000.0) > _gain(flat, 1000.0)


def test_lowpass_matches_scipy_butterworth():
    # a 2nd-order Butterworth lowpass equals the cookbook lowpass with Q = 1/sqrt(2)
    wave = _sine(440.0) + 0.5 * _sine(3000.0)
    filter_ = Filter(FilterType.lowpass, cutoff=1000.0, resonance=1.0 / np.sqrt(2.0), rate=RATE)
    b, a = scipy.signal.butter(2, 1000.0, fs=RATE)
    np.testing.assert_allclose(filter_.apply(wave), scipy.signal.lfilter(b, a, wave), atol=1e-6)


@pytest.mark.parametrize("filter_type", list(FilterType))
def test_constant_cutoff_array_matches_scalar(filter_type):
    wave = np.random.default_rng(0).uniform(-1.0, 1.0, RATE)
    filter_ = Filter(filter_type, cutoff=1500.0, resonance=2.0, rate=RATE)
    np.testing.assert_allclose(filter_.apply(wave, cutoff=np.full(RATE, 1500.0)), filter_.apply(wave), atol=1e-9)


def test_modulated_cutoff():
    wave = np.random.default_rng(0).uniform(-1.0, 1.0, RATE)
    filter_ = Filter(FilterType.lowpass, cutoff=1000.0, resonance=2.0, rate=RATE)
    cutoff = np.linspace(200.0, 5000.0, RATE)
    filtered = filter_.apply(wave, cutoff=cutoff)
    assert filtered.shape == wave.shape
    assert np.isfinite(filtered).all()
    # more high frequency content passes as cutoff rises
    assert np.abs(np.diff(filtered[-2000:])).mean() > 2.0 * np.abs(np.diff(filtered[:2000])).mean()


def test_modulated_cutoff_with_partial_block():
    wave = _sine(440.0, length=0.01)
    filter_ = Filter(FilterType.lowpass, cutoff=1000.0, rate=RATE)
    np.testing.assert_allclose(filter_.apply(wave, cutoff=np.full(wave.size, 1000.0)), filter_.apply(wave))


def test_cutoff_shape_mismatch():
    filter_ = Filter(FilterType.lowpass, rate=RATE)
    with pytest.raises(ValueError):
        filter_.apply(np.zeros(100), cutoff=np.full(50, 1000.0))


def test_empty_wave():
    filter_ = Filter(FilterType.lowpass, rate=RATE)
    assert filter_.apply(np.zeros(0)).size == 0
    assert filter_.apply(np.zeros(0), cutoff=np.zeros(0)).size == 0


@pytest.mark.parametrize(
    "cutoff, expected",
    [
        (-100.0, 10.0),
        (5.0, 10.0),
        (1000.0, 1000.0),
        (8000.0, 0.45 * RATE),
        (20000.0, 0.45 * RATE),
    ],
)
def test_cutoff_is_clamped(cutoff, expected):
    assert Filter(FilterType.lowpass, cutoff=cutoff, rate=RATE).cutoff == expected


def test_resonance_is_clamped():
    assert Filter(FilterType.lowpass, resonance=0.0, rate=RATE).resonance == 0.1


def test_unknown_filter_type():
    with pytest.raises(TypeError):
        Filter("lowpass")


def test_synthesizer_without_filter_is_unchanged():
    raw = Synthesizer(osc1_waveform=Waveform.sawtooth, rate=RATE).generate_constant_wave(440.0, 1.0)
    unfiltered = Synthesizer(osc1_waveform=Waveform.sawtooth, filter_type=None, rate=RATE)
    np.testing.assert_array_equal(unfiltered.generate_constant_wave(440.0, 1.0), raw)


def test_synthesizer_applies_filter_before_envelope():
    synthesizer = Synthesizer(
        osc1_waveform=Waveform.sawtooth,
        filter_type=FilterType.lowpass,
        filter_cutoff=800.0,
        filter_resonance=2.0,
        attack=0.1,
        release=0.1,
        rate=RATE,
    )
    raw = Synthesizer(osc1_waveform=Waveform.sawtooth, attack=0.0, release=0.0, rate=RATE)
    filtered = Filter(FilterType.lowpass, cutoff=800.0, resonance=2.0, rate=RATE).apply(
        raw.generate_constant_wave(440.0, 1.0)
    )
    expected = synthesizer._apply_envelope(filtered)
    np.testing.assert_allclose(synthesizer.generate_constant_wave(440.0, 1.0), expected)


@pytest.mark.parametrize("filter_type", list(FilterType))
def test_synthesizer_filter_envelope_starts_and_ends_at_zero(filter_type):
    synthesizer = Synthesizer(osc1_waveform=Waveform.square, filter_type=filter_type, rate=RATE)
    wave = synthesizer.generate_chord(["C4", "E4", "G4"], 1.0)
    assert wave[0] == 0.0
    assert wave[-1] == 0.0

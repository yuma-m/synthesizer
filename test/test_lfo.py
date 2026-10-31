import numpy as np
import pytest
import scipy.signal

from synthesizer import FilterType, Synthesizer, Waveform

RATE = 16000


def _instantaneous_frequency(wave):
    """frequency of a sine wave estimated from the analytic signal"""
    phases = np.unwrap(np.angle(scipy.signal.hilbert(wave)))
    return np.diff(phases) * RATE / (2.0 * np.pi)


@pytest.mark.parametrize("lfo_waveform", list(Waveform))
def test_zero_depth_is_unchanged(lfo_waveform):
    kwargs = dict(osc1_waveform=Waveform.sawtooth, filter_type=FilterType.lowpass, rate=RATE)
    raw = Synthesizer(**kwargs).generate_constant_wave(440.0, 1.0)
    synthesizer = Synthesizer(lfo_waveform=lfo_waveform, lfo_rate=3.0, **kwargs)
    np.testing.assert_array_equal(synthesizer.generate_constant_wave(440.0, 1.0), raw)


def test_vibrato():
    synthesizer = Synthesizer(lfo_rate=4.0, lfo_pitch_depth=100.0, attack=0.0, release=0.0, rate=RATE)
    wave = synthesizer.generate_constant_wave(440.0, 1.0)
    # ignore edge effects of the Hilbert transform
    frequency = _instantaneous_frequency(wave)[800:-800]
    assert frequency.max() == pytest.approx(440.0 * 2 ** (100 / 1200.0), rel=0.005)
    assert frequency.min() == pytest.approx(440.0 * 2 ** (-100 / 1200.0), rel=0.005)


def test_vibrato_matches_analytic_phase():
    synthesizer = Synthesizer(lfo_rate=5.0, lfo_pitch_depth=50.0, attack=0.0, release=0.0, rate=RATE)
    wave = synthesizer.generate_constant_wave(440.0, 1.0)
    lfo = np.sin(2.0 * np.pi * 5.0 * np.arange(RATE) / RATE)
    phases = np.cumsum(2.0 * np.pi * 440.0 * 2 ** (lfo * 50.0 / 1200.0) / RATE)
    np.testing.assert_allclose(wave, np.sin(phases))


def test_tremolo():
    synthesizer = Synthesizer(lfo_rate=5.0, lfo_amp_depth=0.6, attack=0.0, release=0.0, rate=RATE)
    wave = synthesizer.generate_constant_wave(440.0, 1.0)
    raw = Synthesizer(attack=0.0, release=0.0, rate=RATE).generate_constant_wave(440.0, 1.0)
    lfo = np.sin(2.0 * np.pi * 5.0 * np.arange(RATE) / RATE)
    gain = 1.0 - 0.6 * (1.0 - lfo) / 2.0
    np.testing.assert_allclose(wave, raw * gain)
    assert gain.min() == pytest.approx(0.4, abs=1e-6)
    assert gain.max() == pytest.approx(1.0, abs=1e-6)


@pytest.mark.parametrize("depth, expected", [(-0.5, 0.0), (1.5, 1.0)])
def test_amp_depth_is_clamped(depth, expected):
    synthesizer = Synthesizer(lfo_amp_depth=depth, rate=RATE)
    assert synthesizer._lfo_amp_depth == expected


def test_cutoff_modulation():
    kwargs = dict(
        osc1_waveform=Waveform.sawtooth,
        filter_type=FilterType.lowpass,
        filter_cutoff=800.0,
        filter_resonance=3.0,
        rate=RATE,
    )
    static = Synthesizer(**kwargs).generate_constant_wave(220.0, 1.0)
    wave = Synthesizer(lfo_rate=2.0, lfo_cutoff_depth=2.0, **kwargs).generate_constant_wave(220.0, 1.0)
    assert np.isfinite(wave).all()
    assert not np.allclose(wave, static)
    assert wave[0] == 0.0
    assert wave[-1] == 0.0


def test_cutoff_modulation_without_filter_is_ignored():
    raw = Synthesizer(rate=RATE).generate_constant_wave(440.0, 1.0)
    wave = Synthesizer(lfo_cutoff_depth=2.0, rate=RATE).generate_constant_wave(440.0, 1.0)
    np.testing.assert_array_equal(wave, raw)


def test_sample_and_hold_lfo():
    synthesizer = Synthesizer(lfo_waveform=Waveform.noise, lfo_rate=4.0, rate=RATE, seed=1)
    lfo = synthesizer._lfo(RATE)
    assert np.unique(lfo).size == 4
    for i in range(4):
        block = lfo[i * RATE // 4 : (i + 1) * RATE // 4]
        np.testing.assert_array_equal(block, block[0])
    assert np.abs(lfo).max() <= 1.0


def test_sample_and_hold_lfo_is_reproducible():
    def generate(seed):
        synthesizer = Synthesizer(
            lfo_waveform=Waveform.noise, lfo_rate=8.0, lfo_pitch_depth=200.0, rate=RATE, seed=seed
        )
        return synthesizer.generate_constant_wave(440.0, 1.0)

    np.testing.assert_array_equal(generate(1), generate(1))
    assert not np.array_equal(generate(1), generate(2))


def test_lfo_with_empty_wave():
    synthesizer = Synthesizer(lfo_waveform=Waveform.noise, lfo_pitch_depth=100.0, rate=RATE)
    assert synthesizer.generate_constant_wave(440.0, 0.00001).size == 0


def test_lfo_in_chord():
    synthesizer = Synthesizer(lfo_rate=5.0, lfo_pitch_depth=30.0, lfo_amp_depth=0.5, rate=RATE)
    wave = synthesizer.generate_chord(["C4", "E4", "G4"], 1.0)
    assert np.isfinite(wave).all()
    assert np.abs(wave).max() <= 1.0

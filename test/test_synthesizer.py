import numpy as np
import pytest
import scipy.signal

from synthesizer import Oscillator, Synthesizer, Waveform

RATE = 16000
PERIODIC_WAVEFORMS = [w for w in Waveform if w is not Waveform.noise]


def _phases(frequency, length, rate=RATE):
    return np.cumsum(2.0 * np.pi * frequency / rate * np.ones(int(rate * length)))


@pytest.mark.parametrize("waveform", PERIODIC_WAVEFORMS)
def test_constant_wave(waveform):
    synthesizer = Synthesizer(osc1_waveform=waveform, osc1_volume=1.0, use_osc2=False, rate=RATE)
    wave = synthesizer.generate_constant_wave(440.0, 1.0)
    assert wave.size == RATE
    assert wave.max() == pytest.approx(1.0, abs=1e-3)
    assert wave.min() == pytest.approx(-1.0, abs=1e-3)
    assert wave.mean() == pytest.approx(0.0, abs=1e-3)


@pytest.mark.parametrize(
    "waveform, func",
    [
        (Waveform.sine, np.sin),
        (Waveform.sawtooth, scipy.signal.sawtooth),
        (Waveform.square, scipy.signal.square),
        (Waveform.triangle, lambda t: scipy.signal.sawtooth(t, 0.5)),
    ],
)
def test_oscillator_waveform(waveform, func):
    phases = _phases(440.0, 0.1)
    osc = Oscillator(waveform=waveform, volume=0.5)
    np.testing.assert_allclose(osc.generate_wave(phases), 0.5 * func(phases), atol=1e-12)


@pytest.mark.parametrize(
    "volume, expected",
    [
        (-0.5, 0.0),
        (0.0, 0.0),
        (0.3, 0.3),
        (1.0, 1.0),
        (1.5, 1.0),
    ],
)
def test_oscillator_volume_is_clamped(volume, expected):
    assert Oscillator(waveform=Waveform.sine, volume=volume).volume == expected


def test_oscillator_freq_transpose():
    phases = _phases(440.0, 0.1)
    osc = Oscillator(waveform=Waveform.sine, volume=1.0, freq_transpose=2.0)
    np.testing.assert_allclose(osc.generate_wave(phases), np.sin(phases * 2.0))


def test_oscillator_does_not_modify_phases():
    phases = _phases(440.0, 0.1)
    original = phases.copy()
    Oscillator(waveform=Waveform.sine, volume=1.0, freq_transpose=2.0).generate_wave(phases)
    np.testing.assert_array_equal(phases, original)


@pytest.mark.parametrize("pulse_width", [0.1, 0.25, 0.75])
def test_oscillator_pulse_width(pulse_width):
    phases = _phases(440.0, 0.1)
    osc = Oscillator(waveform=Waveform.square, volume=1.0, pulse_width=pulse_width)
    np.testing.assert_allclose(osc.generate_wave(phases), scipy.signal.square(phases, duty=pulse_width))


@pytest.mark.parametrize(
    "pulse_width, expected",
    [
        (-1.0, 0.01),
        (0.0, 0.01),
        (0.5, 0.5),
        (1.0, 0.99),
    ],
)
def test_oscillator_pulse_width_is_clamped(pulse_width, expected):
    assert Oscillator(waveform=Waveform.square, volume=1.0, pulse_width=pulse_width).pulse_width == expected


def test_pulse_width_does_not_affect_other_waveforms():
    phases = _phases(440.0, 0.1)
    osc = Oscillator(waveform=Waveform.sawtooth, volume=1.0, pulse_width=0.2)
    np.testing.assert_allclose(osc.generate_wave(phases), scipy.signal.sawtooth(phases))


def test_oscillator_noise():
    phases = _phases(440.0, 1.0)
    wave = Oscillator(waveform=Waveform.noise, volume=0.5, seed=1).generate_wave(phases)
    assert wave.size == phases.size
    assert np.abs(wave).max() <= 0.5
    assert np.abs(wave).max() > 0.49
    assert wave.std() == pytest.approx(0.5 / np.sqrt(3.0), rel=0.05)


def test_noise_is_reproducible_with_seed():
    def generate(seed):
        synthesizer = Synthesizer(osc1_waveform=Waveform.noise, rate=RATE, seed=seed)
        return synthesizer.generate_constant_wave(440.0, 1.0)

    np.testing.assert_array_equal(generate(1), generate(1))
    assert not np.array_equal(generate(1), generate(2))


def test_noise_differs_between_oscillators():
    synthesizer = Synthesizer(
        osc1_waveform=Waveform.noise, use_osc2=True, osc2_waveform=Waveform.noise, osc2_volume=1.0, rate=RATE, seed=1
    )
    phases = _phases(440.0, 1.0)
    assert not np.array_equal(synthesizer._osc1.generate_wave(phases), synthesizer._osc2.generate_wave(phases))


def test_noise_differs_between_notes():
    synthesizer = Synthesizer(osc1_waveform=Waveform.noise, rate=RATE, seed=1)
    assert not np.array_equal(
        synthesizer.generate_constant_wave(440.0, 1.0), synthesizer.generate_constant_wave(440.0, 1.0)
    )


def test_oscillator_unknown_waveform():
    osc = Oscillator(waveform="sine", volume=1.0)
    with pytest.raises(TypeError):
        osc.generate_wave(_phases(440.0, 0.1))


def test_constant_wave_matches_analytic_sine():
    synthesizer = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=0.8, attack=0.0, release=0.0, rate=RATE)
    wave = synthesizer.generate_constant_wave(440.0, 1.0)
    np.testing.assert_allclose(wave, 0.8 * np.sin(_phases(440.0, 1.0)))


def test_constant_wave_from_scale():
    synthesizer = Synthesizer(rate=RATE)
    np.testing.assert_allclose(
        synthesizer.generate_constant_wave("A4", 1.0),
        synthesizer.generate_constant_wave(440.0, 1.0),
    )


@pytest.mark.parametrize(
    "length, size",
    [
        (0.5, 8000),
        (1, 16000),
        (0.00001, 0),
        ("2.0", 32000),
    ],
)
def test_constant_wave_length(length, size):
    synthesizer = Synthesizer(rate=RATE)
    assert synthesizer.generate_constant_wave(440.0, length).size == size


def test_default_rate():
    synthesizer = Synthesizer()
    assert synthesizer.generate_constant_wave(440.0, 1.0).size == 44100


def test_osc2_disabled():
    synthesizer = Synthesizer(use_osc2=False, rate=RATE)
    assert synthesizer._osc2 is None


def test_osc2_mix_is_normalized():
    synthesizer = Synthesizer(
        osc1_waveform=Waveform.sawtooth,
        osc1_volume=1.0,
        use_osc2=True,
        osc2_waveform=Waveform.square,
        osc2_volume=0.3,
        osc2_freq_transpose=3.0,
        attack=0.0,
        release=0.0,
        rate=RATE,
    )
    wave = synthesizer.generate_constant_wave(440.0, 1.0)
    phases = _phases(440.0, 1.0)
    expected = (1.0 * scipy.signal.sawtooth(phases) + 0.3 * scipy.signal.square(phases * 3.0)) / 1.3
    np.testing.assert_allclose(wave, expected)
    assert np.abs(wave).max() <= 1.0 + 1e-9


def test_osc2_default_parameters():
    synthesizer = Synthesizer(use_osc2=True, attack=0.0, release=0.0, rate=RATE)
    wave = synthesizer.generate_constant_wave(440.0, 1.0)
    phases = _phases(440.0, 1.0)
    expected = (np.sin(phases) + 0.3 * np.sin(phases * 2.0)) / 1.3
    np.testing.assert_allclose(wave, expected)


@pytest.mark.parametrize(
    "detune, ratio",
    [
        (1200.0, 2.0),
        (-1200.0, 0.5),
        (100.0, 2 ** (1 / 12.0)),
        (0.0, 1.0),
    ],
)
def test_osc2_detune(detune, ratio):
    synthesizer = Synthesizer(
        osc1_volume=0.0,
        use_osc2=True,
        osc2_volume=1.0,
        osc2_freq_transpose=1.5,
        osc2_detune=detune,
        attack=0.0,
        release=0.0,
        rate=RATE,
    )
    wave = synthesizer.generate_constant_wave(440.0, 1.0)
    np.testing.assert_allclose(wave, np.sin(_phases(440.0, 1.0) * 1.5 * ratio), atol=1e-9)


def test_osc_pulse_width_parameters():
    synthesizer = Synthesizer(
        osc1_waveform=Waveform.square,
        osc1_pulse_width=0.2,
        use_osc2=True,
        osc2_waveform=Waveform.square,
        osc2_volume=1.0,
        osc2_pulse_width=0.7,
        attack=0.0,
        release=0.0,
        rate=RATE,
    )
    wave = synthesizer.generate_constant_wave(440.0, 1.0)
    phases = _phases(440.0, 1.0)
    expected = (scipy.signal.square(phases, duty=0.2) + scipy.signal.square(phases * 2.0, duty=0.7)) / 2.0
    np.testing.assert_allclose(wave, expected)


def test_osc2_mix_with_zero_volumes():
    synthesizer = Synthesizer(osc1_volume=0.0, use_osc2=True, osc2_volume=0.0, rate=RATE)
    wave = synthesizer.generate_constant_wave(440.0, 1.0)
    np.testing.assert_array_equal(wave, np.zeros(RATE))


@pytest.mark.parametrize("waveform", list(Waveform))
def test_envelope_starts_and_ends_at_zero(waveform):
    synthesizer = Synthesizer(osc1_waveform=waveform, rate=RATE)
    wave = synthesizer.generate_constant_wave(440.0, 1.0)
    assert wave[0] == 0.0
    assert wave[-1] == 0.0


def test_envelope_shape():
    synthesizer = Synthesizer(attack=0.1, release=0.2, rate=RATE)
    wave = synthesizer.generate_constant_wave(440.0, 1.0)
    raw = Synthesizer(attack=0.0, release=0.0, rate=RATE).generate_constant_wave(440.0, 1.0)
    expected = raw.copy()
    expected[:1600] *= 0.5 - 0.5 * np.cos(np.linspace(0.0, np.pi, 1600))
    expected[-3200:] *= 0.5 + 0.5 * np.cos(np.linspace(0.0, np.pi, 3200))
    np.testing.assert_allclose(wave, expected)
    np.testing.assert_array_equal(wave[1600:-3200], raw[1600:-3200])


def test_default_envelope_length():
    synthesizer = Synthesizer(rate=RATE)
    wave = synthesizer.generate_constant_wave(440.0, 1.0)
    raw = Synthesizer(attack=0.0, release=0.0, rate=RATE).generate_constant_wave(440.0, 1.0)
    # 10ms at 16kHz = 160 samples on each side
    np.testing.assert_array_equal(wave[160:-160], raw[160:-160])
    assert not np.array_equal(wave[:160], raw[:160])
    assert not np.array_equal(wave[-160:], raw[-160:])


def test_envelope_longer_than_wave():
    synthesizer = Synthesizer(attack=1.0, release=1.0, rate=RATE)
    wave = synthesizer.generate_constant_wave(440.0, 0.01)
    assert wave.size == 160
    assert wave[0] == 0.0
    assert wave[-1] == 0.0
    assert np.abs(wave).max() <= 1.0


def test_envelope_disabled():
    synthesizer = Synthesizer(attack=0.0, release=0.0, rate=RATE)
    wave = synthesizer.generate_constant_wave(440.0, 1.0)
    np.testing.assert_allclose(wave, np.sin(_phases(440.0, 1.0)))


def test_negative_envelope_is_treated_as_zero():
    synthesizer = Synthesizer(attack=-1.0, release=-1.0, rate=RATE)
    wave = synthesizer.generate_constant_wave(440.0, 1.0)
    np.testing.assert_allclose(wave, np.sin(_phases(440.0, 1.0)))


def _envelope_of(synthesizer, length=1.0):
    """envelope of synthesizer, measured by applying it to a constant wave"""
    return synthesizer._apply_envelope(np.ones(int(RATE * length)))


def test_adsr_envelope_shape():
    synthesizer = Synthesizer(attack=0.1, decay=0.2, sustain=0.6, release=0.3, rate=RATE)
    envelope = _envelope_of(synthesizer)
    attack = 0.5 - 0.5 * np.cos(np.linspace(0.0, np.pi, 1600))
    decay = 1.0 - 0.4 * (0.5 - 0.5 * np.cos(np.linspace(0.0, np.pi, 3200)))
    release = 0.5 + 0.5 * np.cos(np.linspace(0.0, np.pi, 4800))
    np.testing.assert_allclose(envelope[:1600], attack)
    np.testing.assert_allclose(envelope[1600:4800], decay)
    np.testing.assert_allclose(envelope[4800:11200], 0.6)
    np.testing.assert_allclose(envelope[11200:], 0.6 * release)


def test_adsr_envelope_applied_to_wave():
    synthesizer = Synthesizer(attack=0.1, decay=0.2, sustain=0.6, release=0.3, rate=RATE)
    raw = Synthesizer(attack=0.0, release=0.0, rate=RATE).generate_constant_wave(440.0, 1.0)
    np.testing.assert_allclose(synthesizer.generate_constant_wave(440.0, 1.0), raw * _envelope_of(synthesizer))


def test_decay_without_attack_starts_from_peak():
    envelope = _envelope_of(Synthesizer(attack=0.0, decay=0.1, sustain=0.5, release=0.0, rate=RATE))
    assert envelope[0] == pytest.approx(1.0)
    assert envelope[1599] == pytest.approx(0.5)
    np.testing.assert_allclose(envelope[1600:], 0.5)
    assert np.all(np.diff(envelope[:1600]) <= 0.0)


@pytest.mark.parametrize(
    "sustain, expected",
    [
        (-0.5, 0.0),
        (0.0, 0.0),
        (0.4, 0.4),
        (1.0, 1.0),
        (1.5, 1.0),
    ],
)
def test_sustain_is_clamped(sustain, expected):
    envelope = _envelope_of(Synthesizer(attack=0.0, decay=0.1, sustain=sustain, release=0.0, rate=RATE))
    np.testing.assert_allclose(envelope[1600:], expected)


def test_zero_sustain_silences_tail():
    synthesizer = Synthesizer(attack=0.01, decay=0.1, sustain=0.0, release=0.01, rate=RATE)
    wave = synthesizer.generate_constant_wave(440.0, 1.0)
    np.testing.assert_array_equal(wave[160 + 1600 :], 0.0)


def test_decay_is_cut_off_when_wave_ends():
    synthesizer = Synthesizer(attack=0.0, decay=1.0, sustain=0.0, release=0.0, rate=RATE)
    envelope = _envelope_of(synthesizer, length=0.5)
    full = _envelope_of(synthesizer, length=2.0)
    np.testing.assert_allclose(envelope, full[:8000])


def test_negative_decay_is_treated_as_zero():
    envelope = _envelope_of(Synthesizer(attack=0.0, decay=-1.0, sustain=0.3, release=0.0, rate=RATE))
    np.testing.assert_allclose(envelope, 0.3)


def test_default_envelope_has_full_sustain():
    synthesizer = Synthesizer(rate=RATE)
    np.testing.assert_array_equal(_envelope_of(synthesizer)[160:-160], 1.0)


def test_chord_envelope_starts_and_ends_at_zero():
    synthesizer = Synthesizer(rate=RATE)
    wave = synthesizer.generate_chord(["C4", "E4", "G4"], 1.0)
    assert wave[0] == 0.0
    assert wave[-1] == 0.0


@pytest.mark.parametrize(
    "freqs",
    [
        [261.626, 329.628, 391.995],
        ["C4", "E4", "G4"],
        ["C4", 329.628, "G4", "Bb4"],
        [440.0],
    ],
)
def test_generate_chord(freqs):
    synthesizer = Synthesizer(rate=RATE)
    wave = synthesizer.generate_chord(freqs, 1.0)
    expected = np.mean([synthesizer.generate_constant_wave(f, 1.0) for f in freqs], axis=0)
    assert wave.size == RATE
    np.testing.assert_allclose(wave, expected)
    assert np.abs(wave).max() <= 1.0 + 1e-9


@pytest.mark.parametrize("freqs", [[], None, (440.0, 550.0), 440.0, "C4"])
def test_generate_chord_invalid_freqs(freqs):
    synthesizer = Synthesizer(rate=RATE)
    with pytest.raises(ValueError):
        synthesizer.generate_chord(freqs, 1.0)

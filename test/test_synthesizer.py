# -*- coding: utf-8 -*-

import numpy as np
import pytest
import scipy.signal

from synthesizer import Oscillator, Synthesizer, Waveform

RATE = 16000


def _phases(frequency, length, rate=RATE):
    return np.cumsum(2.0 * np.pi * frequency / rate * np.ones(int(rate * length)))


@pytest.mark.parametrize("waveform", list(Waveform))
def test_constant_wave(waveform):
    synthesizer = Synthesizer(osc1_waveform=waveform, osc1_volume=1.0, use_osc2=False, rate=RATE)
    wave = synthesizer.generate_constant_wave(440.0, 1.0)
    assert wave.size == RATE
    assert wave.max() == pytest.approx(1.0, abs=1e-3)
    assert wave.min() == pytest.approx(-1.0, abs=1e-3)
    assert wave.mean() == pytest.approx(0.0, abs=1e-3)


@pytest.mark.parametrize("waveform, func", [
    (Waveform.sine, np.sin),
    (Waveform.sawtooth, scipy.signal.sawtooth),
    (Waveform.square, scipy.signal.square),
    (Waveform.triangle, lambda t: scipy.signal.sawtooth(t, 0.5)),
])
def test_oscillator_waveform(waveform, func):
    phases = _phases(440.0, 0.1)
    osc = Oscillator(waveform=waveform, volume=0.5)
    np.testing.assert_allclose(osc.generate_wave(phases), 0.5 * func(phases), atol=1e-12)


@pytest.mark.parametrize("volume, expected", [
    (-0.5, 0.0),
    (0.0, 0.0),
    (0.3, 0.3),
    (1.0, 1.0),
    (1.5, 1.0),
])
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


@pytest.mark.parametrize("length, size", [
    (0.5, 8000),
    (1, 16000),
    (0.00001, 0),
    ("2.0", 32000),
])
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
        osc1_waveform=Waveform.sawtooth, osc1_volume=1.0,
        use_osc2=True, osc2_waveform=Waveform.square,
        osc2_volume=0.3, osc2_freq_transpose=3.0,
        attack=0.0, release=0.0, rate=RATE,
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


def test_chord_envelope_starts_and_ends_at_zero():
    synthesizer = Synthesizer(rate=RATE)
    wave = synthesizer.generate_chord(["C4", "E4", "G4"], 1.0)
    assert wave[0] == 0.0
    assert wave[-1] == 0.0


@pytest.mark.parametrize("freqs", [
    [261.626, 329.628, 391.995],
    ["C4", "E4", "G4"],
    ["C4", 329.628, "G4", "Bb4"],
    [440.0],
])
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

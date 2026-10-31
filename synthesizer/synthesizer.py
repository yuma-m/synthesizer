from enum import Enum

import numpy as np
import scipy.signal

from .filter import Filter
from .frequency import frequency_from_scale


def _triangle(phases):
    """triangle wave with period 2*pi, rising from -1 at phase 0 to 1 at phase pi"""
    cycle = np.mod(phases / (2.0 * np.pi), 1.0)
    return 1.0 - 4.0 * np.abs(cycle - 0.5)


def _raised_cosine(size):
    """smooth ramp rising from 0 to 1, which causes less click noise than a linear ramp"""
    return 0.5 - 0.5 * np.cos(np.linspace(0.0, np.pi, size))


class Waveform(Enum):
    sine = "sine"
    sawtooth = "sawtooth"
    square = "square"
    triangle = "triangle"
    noise = "noise"


class Oscillator:
    """Virtual oscillator object

    :param Waveform _waveform: waveform of oscillator
    :param float _volume: amplitude of generated wave (0.0 - 1.0)
    :param float _freq_transpose: transpose of frequency (for sub oscillator)
    :param float _pulse_width: duty cycle of square wave (0.01 - 0.99)
    :param numpy.random.Generator _rng: random generator for noise waveform
    """

    def __init__(self, waveform, volume, freq_transpose=1.0, pulse_width=0.5, seed=None):
        self._waveform = waveform
        self._volume = max(0.0, min(1.0, volume))
        self._freq_transpose = freq_transpose
        self._pulse_width = max(0.01, min(0.99, pulse_width))
        self._rng = np.random.default_rng(seed)

    @property
    def volume(self):
        return self._volume

    @property
    def pulse_width(self):
        return self._pulse_width

    def _wave_func(self, phases):
        if self._waveform is Waveform.sine:
            return np.sin(phases)
        elif self._waveform is Waveform.sawtooth:
            return scipy.signal.sawtooth(phases)
        elif self._waveform is Waveform.square:
            return scipy.signal.square(phases, duty=self._pulse_width)
        elif self._waveform is Waveform.triangle:
            return _triangle(phases)
        elif self._waveform is Waveform.noise:
            # white noise does not depend on phases
            return self._rng.uniform(-1.0, 1.0, np.shape(phases))
        raise TypeError(f"unknown waveform: {self._waveform}")

    def generate_wave(self, phases):
        phases = np.copy(phases) * self._freq_transpose
        return self._volume * self._wave_func(phases)


class Synthesizer:
    """Virtual analog synthesizer object

    :param Oscillator _osc1: main virtual oscillator
    :param (Oscillator|None) _osc2: sub virtual oscillator
    :param (Filter|None) _filter: virtual filter applied to the oscillators
    """

    def __init__(
        self,
        osc1_waveform=Waveform.sine,
        osc1_volume=1.0,
        osc1_pulse_width=0.5,
        use_osc2=False,
        osc2_waveform=Waveform.sine,
        osc2_volume=0.3,
        osc2_freq_transpose=2.0,
        osc2_detune=0.0,
        osc2_pulse_width=0.5,
        filter_type=None,
        filter_cutoff=1000.0,
        filter_resonance=0.707,
        lfo_waveform=Waveform.sine,
        lfo_rate=5.0,
        lfo_pitch_depth=0.0,
        lfo_amp_depth=0.0,
        lfo_cutoff_depth=0.0,
        attack=0.01,
        decay=0.0,
        sustain=1.0,
        release=0.01,
        rate=44100,
        seed=None,
    ):
        """Constructor of Synthesizer

        :param Waveform osc1_waveform: waveform for oscillator 1
        :param float osc1_volume: relative volume of oscillator 1
        :param float osc1_pulse_width: duty cycle of square wave for oscillator 1 (0.01 - 0.99)
        :param bool use_osc2: if True wave from osc2 is added to wave from osc1
        :param Waveform osc2_waveform: waveform for oscillator 2
        :param float osc2_volume: relative volume of oscillator 2
        :param float osc2_freq_transpose: frequency transpose for oscillator 2
        :param float osc2_detune: fine tuning of oscillator 2 (cents)
        :param float osc2_pulse_width: duty cycle of square wave for oscillator 2 (0.01 - 0.99)
        :param (FilterType|None) filter_type: type of filter applied to the oscillators, None disables filter
        :param float filter_cutoff: cutoff frequency of filter (Hz)
        :param float filter_resonance: resonance (Q factor) of filter, 0.707 gives a flat response.
                                       high resonance may push peaks beyond [-1.0, 1.0]
        :param Waveform lfo_waveform: waveform of LFO, noise gives a random value per LFO cycle (sample and hold)
        :param float lfo_rate: frequency of LFO (Hz)
        :param float lfo_pitch_depth: depth of pitch modulation by LFO (cents), aka vibrato
        :param float lfo_amp_depth: depth of amplitude modulation by LFO (0.0 - 1.0), aka tremolo
        :param float lfo_cutoff_depth: depth of filter cutoff modulation by LFO (octaves)
        :param float attack: fade-in time of each wave (seconds), prevents click noise at the start
        :param float decay: time to fall from the peak to the sustain level after attack (seconds)
        :param float sustain: level held after decay until release (0.0 - 1.0)
        :param float release: fade-out time at the end of each wave (seconds), prevents click noise at the end.
                              the release is included in the length of the wave
        :param int rate: sampling rate
        :param (int|None) seed: random seed for noise waveform, makes noise reproducible
        """
        # spawn independent random streams so that osc1, osc2 and LFO noise are not identical
        osc1_seed, osc2_seed, lfo_seed = np.random.SeedSequence(seed).spawn(3)
        self._osc1 = Oscillator(
            waveform=osc1_waveform, volume=osc1_volume, pulse_width=osc1_pulse_width, seed=osc1_seed
        )
        self._use_osc2 = use_osc2
        if self._use_osc2:
            self._osc2 = Oscillator(
                waveform=osc2_waveform,
                volume=osc2_volume,
                freq_transpose=osc2_freq_transpose * 2 ** (osc2_detune / 1200.0),
                pulse_width=osc2_pulse_width,
                seed=osc2_seed,
            )
        else:
            self._osc2 = None
        if filter_type is None:
            self._filter = None
        else:
            self._filter = Filter(filter_type, cutoff=filter_cutoff, resonance=filter_resonance, rate=rate)
        self._lfo_waveform = lfo_waveform
        self._lfo_osc = Oscillator(waveform=lfo_waveform, volume=1.0)
        self._lfo_rng = np.random.default_rng(lfo_seed)
        self._lfo_rate = max(0.0, lfo_rate)
        self._lfo_pitch_depth = lfo_pitch_depth
        self._lfo_amp_depth = max(0.0, min(1.0, lfo_amp_depth))
        self._lfo_cutoff_depth = lfo_cutoff_depth if self._filter is not None else 0.0
        self._attack = max(0.0, attack)
        self._decay = max(0.0, decay)
        self._sustain = max(0.0, min(1.0, sustain))
        self._release = max(0.0, release)
        self._rate = rate

    def _generate_wave(self, phases):
        wave = self._osc1.generate_wave(phases)
        if self._use_osc2:
            wave += self._osc2.generate_wave(phases)
            total_volume = self._osc1.volume + self._osc2.volume
            if total_volume > 0.0:
                wave /= total_volume
        return wave

    def _lfo(self, size):
        """LFO signal in [-1.0, 1.0], restarted at phase 0 for each wave"""
        times = np.arange(size) / self._rate
        if self._lfo_waveform is Waveform.noise:
            # sample and hold: a new random value for each LFO cycle
            cycles = np.floor(times * self._lfo_rate).astype(int)
            return self._lfo_rng.uniform(-1.0, 1.0, cycles[-1] + 1 if size else 0)[cycles]
        return self._lfo_osc.generate_wave(2.0 * np.pi * self._lfo_rate * times)

    def _envelope(self, size):
        """ADSR envelope; release is applied multiplicatively so it starts from the current level"""
        attack = min(int(self._rate * self._attack), size)
        decay = int(self._rate * self._decay)
        release = min(int(self._rate * self._release), size)
        envelope = np.full(size, self._sustain)
        envelope[:attack] = _raised_cosine(attack)
        # decay is cut off (not compressed) if the wave ends before it completes
        decay_part = envelope[attack : attack + decay]
        decay_part[:] = (1.0 - (1.0 - self._sustain) * _raised_cosine(decay))[: decay_part.size]
        if release > 0:
            envelope[-release:] *= _raised_cosine(release)[::-1]
        return envelope

    def _apply_envelope(self, wave):
        wave *= self._envelope(wave.size)
        return wave

    def generate_constant_wave(self, frequency, length):
        """generate wave with constant frequency

        :param (float|str) frequency: frequency or scale of wave
        :param float length: length of wave (seconds)
        :rtype: numpy.array
        :return: normalized wave
        """
        if isinstance(frequency, str):
            frequency = frequency_from_scale(frequency)
        size = int(self._rate * float(length))
        use_lfo = self._lfo_pitch_depth != 0.0 or self._lfo_amp_depth > 0.0 or self._lfo_cutoff_depth != 0.0
        lfo = self._lfo(size) if use_lfo else None

        frequencies = frequency * np.ones(size)
        if self._lfo_pitch_depth != 0.0:
            frequencies *= 2 ** (lfo * self._lfo_pitch_depth / 1200.0)
        phases = np.cumsum(2.0 * np.pi * frequencies / self._rate)
        wave = self._generate_wave(phases)
        if self._filter is not None:
            cutoff = None
            if self._lfo_cutoff_depth != 0.0:
                cutoff = self._filter.cutoff * 2 ** (lfo * self._lfo_cutoff_depth)
            wave = self._filter.apply(wave, cutoff=cutoff)
        if self._lfo_amp_depth > 0.0:
            wave *= 1.0 - self._lfo_amp_depth * (1.0 - lfo) / 2.0
        return self._apply_envelope(wave)

    def generate_chord(self, freqs, length):
        """generate wave consists of multiple frequencies

        :param list[float] freqs: list of frequencies or scales
        :param float length: length of wave (seconds)
        :rtype: numpy.array
        :return: normalized wave
        """
        if not freqs or not isinstance(freqs, list):
            raise ValueError("freqs must be a list of float")
        wave = self.generate_constant_wave(freqs[0], length)
        for freq in freqs[1:]:
            wave += self.generate_constant_wave(freq, length)
        wave /= len(freqs)
        return wave

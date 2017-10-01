# -*- coding: utf-8 -*-

import numpy as np
import scipy.signal
from enum import Enum


class Waveform(Enum):
    sine = "sine"
    sawtooth = "sawtooth"
    square = "square"


class Oscillator(object):
    u""" Virtual oscillator object

     :param Waveform _waveform: waveform of oscillator
     :param float _volume: amplitude of generated wave (0.1 - 1.0)
     :param float _freq_transpose: transpose of frequency (for sub oscillator)
     """

    def __init__(self, waveform, volume, freq_transpose=1.0):
        self._waveform = waveform
        self._volume = max(0.0, min(1.0, volume))
        self._freq_transpose = freq_transpose

    @property
    def volume(self):
        return self._volume

    @property
    def _wave_func(self):
        if self._waveform is Waveform.sine:
            return np.sin
        elif self._waveform is Waveform.sawtooth:
            return scipy.signal.sawtooth
        elif self._waveform is Waveform.square:
            return scipy.signal.square
        raise TypeError("unknown waveform: {}".format(self._waveform))

    def generate_wave(self, phases):
        phases = np.copy(phases) * self._freq_transpose
        return self._volume * self._wave_func(phases)


class Synthesizer(object):
    u""" Virtual analog synthesizer object

    :param Oscillator _osc1: main virtual oscillator
    :param (Oscillator|None) _osc2: sub virtual oscillator
    """

    def __init__(self, osc1_waveform=Waveform.sine, osc1_volume=1.0,
                 use_osc2=False, osc2_waveform=Waveform.sine,
                 osc2_volume=0.3, osc2_freq_transpose=2.0,
                 rate=44100):
        u""" Constructor of Synthesizer

        :param Waveform osc1_waveform: waveform for oscillator 1
        :param float osc1_volume: relative volume of oscillator 1
        :param bool use_osc2: if True wave from osc2 is added to wave from osc1
        :param Waveform osc2_waveform: waveform for oscillator 2
        :param float osc2_volume: relative volume of oscillator 2
        :param float osc2_freq_transpose: frequency transpose for oscillator 2
        :param int rate: sampling ratio
        """
        self._osc1 = Oscillator(waveform=osc1_waveform, volume=osc1_volume)
        self._use_osc2 = use_osc2
        if self._use_osc2:
            self._osc2 = Oscillator(waveform=osc2_waveform, volume=osc2_volume, freq_transpose=osc2_freq_transpose)
        else:
            self._osc2 = None
        self._rate = rate

    def _generate_wave(self, phases):
        wave = self._osc1.generate_wave(phases)
        if self._use_osc2:
            wave += self._osc2.generate_wave(phases)
            wave *= (1.0 / (self._osc1.volume + self._osc2.volume))
        return wave

    def generate_constant_wave(self, frequency, length):
        u""" generate wave with constant frequency

        :param float frequency: frequency of wave
        :param float length: length of wave (seconds)
        :rtype: numpy.array
        :return: normalized wave
        """
        phases = np.cumsum(2.0 * np.pi * frequency / self._rate * np.ones(int(self._rate * float(length))))
        return self._generate_wave(phases)

    def generate_chord(self, freqs, length):
        u""" generate wave consists of multiple frequencies

        :param list[float] freqs: list of frequencies
        :param length: legnth of wave (seconds)
        :rtype: numpy.array
        :return: normalized wave
        """
        if not freqs or not isinstance(freqs, list):
            raise ValueError("freqs must be a list of float")
        wave = self.generate_constant_wave(freqs[0], length)
        for freq in freqs[1:]:
            wave += self.generate_constant_wave(freq, length)
        wave /= float(len(freqs))
        return wave

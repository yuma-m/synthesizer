from enum import Enum

import numpy as np
import scipy.signal

MIN_CUTOFF = 10.0
MIN_RESONANCE = 0.1
# cutoff frequencies are updated per block of samples when they are modulated
BLOCK_SIZE = 64


class FilterType(Enum):
    lowpass = "lowpass"
    highpass = "highpass"
    bandpass = "bandpass"


class Filter:
    """ Virtual 2-pole (12 dB/oct) resonant filter

    Coefficients follow the Audio EQ Cookbook by Robert Bristow-Johnson.

    :param FilterType _filter_type: type of filter
    :param float _cutoff: cutoff frequency (Hz)
    :param float _resonance: resonance as Q factor (0.707 gives a flat response)
    :param int _rate: sampling rate
    """

    def __init__(self, filter_type, cutoff=1000.0, resonance=0.707, rate=44100):
        if not isinstance(filter_type, FilterType):
            raise TypeError(f"unknown filter type: {filter_type}")
        self._filter_type = filter_type
        self._rate = rate
        self._cutoff = self._clamp_cutoff(cutoff)
        self._resonance = max(MIN_RESONANCE, resonance)

    @property
    def cutoff(self):
        return self._cutoff

    @property
    def resonance(self):
        return self._resonance

    def _clamp_cutoff(self, cutoff):
        return np.clip(cutoff, MIN_CUTOFF, 0.45 * self._rate)

    def _coefficients(self, cutoff):
        """ biquad coefficients for scalar or array of cutoff frequencies

        :return: (b, a) whose last axis holds the 3 coefficients
        """
        w0 = 2.0 * np.pi * np.asarray(cutoff, dtype=float) / self._rate
        cos_w0 = np.cos(w0)
        alpha = np.sin(w0) / (2.0 * self._resonance)
        if self._filter_type is FilterType.lowpass:
            b = [(1.0 - cos_w0) / 2.0, 1.0 - cos_w0, (1.0 - cos_w0) / 2.0]
        elif self._filter_type is FilterType.highpass:
            b = [(1.0 + cos_w0) / 2.0, -(1.0 + cos_w0), (1.0 + cos_w0) / 2.0]
        else:
            # constant 0 dB peak gain
            b = [alpha, np.zeros_like(alpha), -alpha]
        a = [1.0 + alpha, -2.0 * cos_w0, 1.0 - alpha]
        a0 = a[0]
        return np.stack(b, axis=-1) / a0[..., None], np.stack(a, axis=-1) / a0[..., None]

    def apply(self, wave, cutoff=None):
        """ filter wave

        :param numpy.array wave: wave to be filtered
        :param (float|numpy.array|None) cutoff: cutoff frequency, or cutoff per sample for modulation.
                                                cutoff of the filter is used if None
        :rtype: numpy.array
        :return: filtered wave (resonance may push peaks beyond [-1.0, 1.0])
        """
        if cutoff is None:
            cutoff = self._cutoff
        cutoff = self._clamp_cutoff(cutoff)
        if np.ndim(cutoff) == 0:
            b, a = self._coefficients(cutoff)
            return scipy.signal.lfilter(b, a, wave)
        if np.shape(cutoff) != np.shape(wave):
            raise ValueError("cutoff must have the same shape as wave")
        filtered = np.empty_like(wave, dtype=float)
        starts = np.arange(0, wave.size, BLOCK_SIZE)
        if starts.size == 0:
            return filtered
        b, a = self._coefficients(np.add.reduceat(cutoff, starts) / np.diff(np.append(starts, wave.size)))
        state = np.zeros(2)
        for i, start in enumerate(starts):
            block = slice(start, start + BLOCK_SIZE)
            filtered[block], state = scipy.signal.lfilter(b[i], a[i], wave[block], zi=state)
        return filtered

# -*- coding: utf-8 -*-

import numpy as np
from scipy.io import wavfile


class Writer(object):

    def __init__(self, rate=44100):
        self._rate = rate

    def write_wave(self, file_path, wave):
        u""" write wave to a wav file

        :param str file_path: relative / absolute path of wave file
        :param numpy.array wave: normalized wave
        """
        wave = (wave * float(2 ** 15 - 1)).astype(np.int16)
        wavfile.write(file_path, self._rate, wave)

    def write_waves(self, file_path, *waves):
        u""" write waves to a wav file

        :param str file_path: relative / absolute path of wave file
        :param list[numpy.array] waves: list of normalized waves
        """
        self.write_wave(file_path, np.concatenate(waves))

import numpy as np
from scipy.io import wavfile

from .utils import to_int16


class Writer:
    def __init__(self, rate=44100):
        self._rate = rate

    def write_wave(self, file_path, wave):
        """write wave to a wav file

        :param str file_path: relative / absolute path of wave file
        :param numpy.array wave: normalized wave
        """
        wavfile.write(file_path, self._rate, to_int16(wave))

    def write_waves(self, file_path, *waves):
        """write waves to a wav file

        :param str file_path: relative / absolute path of wave file
        :param list[numpy.array] waves: list of normalized waves
        """
        self.write_wave(file_path, np.concatenate(waves))

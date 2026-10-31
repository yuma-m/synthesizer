import os

import numpy as np
from scipy.io import wavfile

from .utils import Wave, to_int16


class Writer:
    def __init__(self, rate: int = 44100) -> None:
        self._rate = rate

    def write_wave(self, file_path: str | os.PathLike[str], wave: Wave) -> None:
        """write wave to a wav file

        :param file_path: relative / absolute path of wave file
        :param wave: normalized wave
        """
        wavfile.write(file_path, self._rate, to_int16(wave))

    def write_waves(self, file_path: str | os.PathLike[str], *waves: Wave) -> None:
        """write waves to a wav file

        :param file_path: relative / absolute path of wave file
        :param waves: normalized waves, concatenated in order
        """
        self.write_wave(file_path, np.concatenate(waves))

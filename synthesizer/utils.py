import numpy as np


def to_int16(wave):
    """convert normalized wave to 16-bit PCM

    Samples outside [-1.0, 1.0] are clipped to avoid integer overflow.

    :param numpy.array wave: normalized wave
    :rtype: numpy.array
    :return: wave as int16 array
    """
    return (np.clip(wave, -1.0, 1.0) * (2**15 - 1)).astype(np.int16)

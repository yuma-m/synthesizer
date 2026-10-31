from typing import TypeAlias

import numpy as np
from numpy.typing import NDArray

Wave: TypeAlias = NDArray[np.float64]
"""Normalized wave: a 1-D float array whose samples are nominally in [-1.0, 1.0]"""


def to_int16(wave: Wave) -> NDArray[np.int16]:
    """convert normalized wave to 16-bit PCM

    Samples outside [-1.0, 1.0] are clipped to avoid integer overflow.

    :param wave: normalized wave
    :return: wave as int16 array
    """
    return (np.clip(wave, -1.0, 1.0) * (2**15 - 1)).astype(np.int16)

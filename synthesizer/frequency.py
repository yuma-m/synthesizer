A1_FREQ = 55.0

BASE_FREQUENCY = {
    "C": A1_FREQ * 2 ** (-9 / 12),
    "C#": A1_FREQ * 2 ** (-8 / 12),
    "Db": A1_FREQ * 2 ** (-8 / 12),
    "D": A1_FREQ * 2 ** (-7 / 12),
    "D#": A1_FREQ * 2 ** (-6 / 12),
    "Eb": A1_FREQ * 2 ** (-6 / 12),
    "E": A1_FREQ * 2 ** (-5 / 12),
    "F": A1_FREQ * 2 ** (-4 / 12),
    "F#": A1_FREQ * 2 ** (-3 / 12),
    "Gb": A1_FREQ * 2 ** (-3 / 12),
    "G": A1_FREQ * 2 ** (-2 / 12),
    "G#": A1_FREQ * 2 ** (-1 / 12),
    "Ab": A1_FREQ * 2 ** (-1 / 12),
    "A": A1_FREQ,
    "A#": A1_FREQ * 2 ** (1 / 12),
    "Bb": A1_FREQ * 2 ** (1 / 12),
    "B": A1_FREQ * 2 ** (2 / 12),
}


def frequency_from_scale(scale):
    """ Calculate frequency from pitch

    :param str scale: e.g. C4, Ab3, D#5
    :rtype: float
    :return: Frequency of pitch
    """
    base, octave = scale[:-1], scale[-1]
    octave = int(octave)
    if base not in BASE_FREQUENCY:
        return ValueError("Unknown note: {}".format(base))
    return BASE_FREQUENCY[base] * 2 ** (octave - 1)

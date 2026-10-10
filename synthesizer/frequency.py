import re

A1_FREQ = 55.0

BASE_FREQUENCY = {
    "C": A1_FREQ * 2 ** (-9 / 12.0),
    "C#": A1_FREQ * 2 ** (-8 / 12.0),
    "Db": A1_FREQ * 2 ** (-8 / 12.0),
    "D": A1_FREQ * 2 ** (-7 / 12.0),
    "D#": A1_FREQ * 2 ** (-6 / 12.0),
    "Eb": A1_FREQ * 2 ** (-6 / 12.0),
    "E": A1_FREQ * 2 ** (-5 / 12.0),
    "F": A1_FREQ * 2 ** (-4 / 12.0),
    "F#": A1_FREQ * 2 ** (-3 / 12.0),
    "Gb": A1_FREQ * 2 ** (-3 / 12.0),
    "G": A1_FREQ * 2 ** (-2 / 12.0),
    "G#": A1_FREQ * 2 ** (-1 / 12.0),
    "Ab": A1_FREQ * 2 ** (-1 / 12.0),
    "A": A1_FREQ,
    "A#": A1_FREQ * 2 ** (1 / 12.0),
    "Bb": A1_FREQ * 2 ** (1 / 12.0),
    "B": A1_FREQ * 2 ** (2 / 12.0),
}

_SCALE_PATTERN = re.compile(r"^([A-G][#b]?)(-?\d+)$")


def frequency_from_scale(scale):
    """ Calculate frequency from pitch

    :param str scale: e.g. C4, Ab3, D#5
    :rtype: float
    :return: Frequency of pitch
    """
    match = _SCALE_PATTERN.match(scale)
    if not match:
        raise ValueError("Invalid scale: {}".format(scale))
    base, octave = match.group(1), int(match.group(2))
    if base not in BASE_FREQUENCY:
        raise ValueError("Unknown note: {}".format(base))
    return BASE_FREQUENCY[base] * 2 ** (octave - 1)

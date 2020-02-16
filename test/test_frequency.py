# -*- coding: utf-8 -*-

from nose.tools import assert_almost_equal
from parameterized import parameterized

from synthesizer.frequency import frequency_from_scale


@parameterized([
    ("A0", 27.5),
    ("A#0", 29.135),
    ("Bb0", 29.135),
    ("B0", 30.868),
    ("C1", 32.703),
    ("C#1", 34.648),
    ("Db1", 34.648),
    ("D1", 36.708),
    ("D#1", 38.891),
    ("Eb1", 38.891),
    ("E1", 41.203),
    ("F1", 43.654),
    ("F#1", 46.249),
    ("Gb1", 46.249),
    ("G1", 48.999),
    ("G#1", 51.913),
    ("Ab1", 51.913),
    ("A1", 55),
    ("C3", 130.813),
    ("A4", 440),
    ("E5", 659.255),
])
def test_frequency_from_scale(scale, frequency):
    assert_almost_equal(frequency_from_scale(scale), frequency, places=3)

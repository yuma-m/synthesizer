# -*- coding: utf-8 -*-

from synthesizer import Synthesizer, Waveform
from nose.tools import eq_, assert_almost_equal

RATE = 16000


def test_sine_wave():
    synthesizer = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False, rate=RATE)
    wave = synthesizer.generate_constant_wave(440.0, 1.0)
    eq_(wave.size, RATE)
    assert_almost_equal(wave.max(), 1.0, places=3)
    assert_almost_equal(wave.min(), -1.0, places=3)
    assert_almost_equal(wave.mean(), 0.0, places=3)


def test_sawtooth_wave():
    synthesizer = Synthesizer(osc1_waveform=Waveform.sawtooth, osc1_volume=1.0, use_osc2=False, rate=RATE)
    wave = synthesizer.generate_constant_wave(440.0, 1.0)
    eq_(wave.size, RATE)
    assert_almost_equal(wave.max(), 1.0, places=3)
    assert_almost_equal(wave.min(), -1.0, places=3)
    assert_almost_equal(wave.mean(), 0.0, places=3)


def test_square_wave():
    synthesizer = Synthesizer(osc1_waveform=Waveform.square, osc1_volume=1.0, use_osc2=False, rate=RATE)
    wave = synthesizer.generate_constant_wave(440.0, 1.0)
    eq_(wave.size, RATE)
    assert_almost_equal(wave.max(), 1.0, places=3)
    assert_almost_equal(wave.min(), -1.0, places=3)
    assert_almost_equal(wave.mean(), 0.0, places=3)

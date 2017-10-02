# -*- coding: utf-8 -*-

import os

from nose.tools import ok_

from synthesizer import Synthesizer, Waveform, Writer


def teardown_write_wave():
    os.remove("./test_wave.wav")


def test_write_wave():
    writer = Writer()

    synthesizer = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
    wave = synthesizer.generate_constant_wave(440.0, 3.0)

    writer.write_wave("./test_wave.wav", wave)
    ok_("write_wave() succeeded.")


test_write_wave.teardown = teardown_write_wave


def teardown_write_waves():
    os.remove("./test_waves.wav")


def test_write_waves():
    writer = Writer()

    synthesizer = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
    wave1 = synthesizer.generate_constant_wave(220.0, 3.0)
    wave2 = synthesizer.generate_constant_wave(440.0, 3.0)

    writer.write_waves("./test_waves.wav", wave1, wave2)
    ok_("write_waves() succeeded.")


test_write_waves.teardown = teardown_write_waves

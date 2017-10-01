#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from synthesizer import Player, Synthesizer, Waveform


def main():
    player = Player()
    player.open_stream()

    print("play sine wave")
    synthesizer = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
    player.play_wave(synthesizer.generate_constant_wave(440.0, 3.0))
    time.sleep(0.5)

    print("play square wave")
    synthesizer = Synthesizer(osc1_waveform=Waveform.square, osc1_volume=0.8, use_osc2=False)
    player.play_wave(synthesizer.generate_constant_wave(440.0, 3.0))
    time.sleep(0.5)

    print("play synthesized wave 1")
    synthesizer = Synthesizer(
        osc1_waveform=Waveform.sawtooth, osc1_volume=1.0,
        use_osc2=True, osc2_waveform=Waveform.sawtooth,
        osc2_volume=0.3, osc2_freq_transpose=6.0,
    )
    player.play_wave(synthesizer.generate_constant_wave(440.0, 3.0))
    time.sleep(0.5)

    print("play synthesized wave 2")
    synthesizer = Synthesizer(
        osc1_waveform=Waveform.square, osc1_volume=1.0,
        use_osc2=True, osc2_waveform=Waveform.sine,
        osc2_volume=0.3, osc2_freq_transpose=3.0,
    )
    player.play_wave(synthesizer.generate_constant_wave(440.0, 3.0))


if __name__ == '__main__':
    main()

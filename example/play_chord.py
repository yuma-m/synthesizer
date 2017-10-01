#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from synthesizer import Player, Synthesizer, Waveform


BASE = 261.626  # C4


def main():
    player = Player()
    player.open_stream()

    print("play major chord")
    synthesizer = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
    chord = [BASE,  BASE * 2.0 ** (4 / 12.0), BASE * 2.0 ** (7 / 12.0)]
    player.play_wave(synthesizer.generate_chord(chord, 3.0))
    time.sleep(0.5)

    print("play minor chord")
    chord = [BASE,  BASE * 2.0 ** (3 / 12.0), BASE * 2.0 ** (7 / 12.0)]
    player.play_wave(synthesizer.generate_chord(chord, 3.0))
    time.sleep(0.5)

    print("play sus4 chord")
    chord = [BASE,  BASE * 2.0 ** (5 / 12.0), BASE * 2.0 ** (7 / 12.0)]
    player.play_wave(synthesizer.generate_chord(chord, 3.0))
    time.sleep(0.5)

    print("play 7th chord")
    chord = [BASE,  BASE * 2.0 ** (4 / 12.0), BASE * 2.0 ** (7 / 12.0), BASE * 2.0 ** (10 / 12.0)]
    player.play_wave(synthesizer.generate_chord(chord, 3.0))
    time.sleep(0.5)

    print("play add9 chord")
    chord = [BASE,  BASE * 2.0 ** (4 / 12.0), BASE * 2.0 ** (7 / 12.0), BASE * 2.0 ** (14 / 12.0)]
    player.play_wave(synthesizer.generate_chord(chord, 3.0))
    time.sleep(0.5)

    print("play chord sequence")
    chord = [BASE * 2.0 ** (2 / 12.0),  BASE * 2.0 ** (5 / 12.0), BASE * 2.0 ** (9 / 12.0), BASE * 2.0 ** (12 / 12.0)]
    player.play_wave(synthesizer.generate_chord(chord, 1.0))
    chord = [BASE * 2.0 ** (2 / 12.0),  BASE * 2.0 ** (7 / 12.0), BASE * 2.0 ** (11 / 12.0)]
    player.play_wave(synthesizer.generate_chord(chord, 1.0))
    chord = [BASE,  BASE * 2.0 ** (4 / 12.0), BASE * 2.0 ** (7 / 12.0), BASE * 2.0 ** (12 / 12.0)]
    player.play_wave(synthesizer.generate_chord(chord, 1.0))


if __name__ == '__main__':
    main()

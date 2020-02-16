#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from synthesizer import Player, Synthesizer, Waveform


def main():
    player = Player()
    player.open_stream()

    print("play major chord")
    synthesizer = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
    chord = ["C4", "E4", "G4"]
    player.play_wave(synthesizer.generate_chord(chord, 3.0))
    time.sleep(0.5)

    print("play minor chord")
    chord = ["C4", "Eb4", "G4"]
    player.play_wave(synthesizer.generate_chord(chord, 3.0))
    time.sleep(0.5)

    print("play sus4 chord")
    chord = ["C4", "F4", "G4"]
    player.play_wave(synthesizer.generate_chord(chord, 3.0))
    time.sleep(0.5)

    print("play 7th chord")
    chord = ["C4", "E4", "G4", "Bb4"]
    player.play_wave(synthesizer.generate_chord(chord, 3.0))
    time.sleep(0.5)

    print("play add9 chord")
    chord = ["C4", "E4", "G4", "D5"]
    player.play_wave(synthesizer.generate_chord(chord, 3.0))
    time.sleep(0.5)

    print("play chord sequence")
    chord = ["D4", "F4", "A4", "C5"]
    player.play_wave(synthesizer.generate_chord(chord, 1.0))
    chord = ["D4", "G4", "B4"]
    player.play_wave(synthesizer.generate_chord(chord, 1.0))
    chord = ["E4", "G4", "C5"]
    player.play_wave(synthesizer.generate_chord(chord, 1.0))


if __name__ == '__main__':
    main()

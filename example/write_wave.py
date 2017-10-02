#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from synthesizer import Synthesizer, Waveform, Writer


BASE = 261.626  # C4
DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    writer = Writer()

    print("write chord sequence")
    synthesizer = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
    chord = [BASE * 2.0 ** (2 / 12.0),  BASE * 2.0 ** (5 / 12.0), BASE * 2.0 ** (9 / 12.0), BASE * 2.0 ** (12 / 12.0)]
    wave1 = synthesizer.generate_chord(chord, 1.0)
    chord = [BASE * 2.0 ** (2 / 12.0),  BASE * 2.0 ** (7 / 12.0), BASE * 2.0 ** (11 / 12.0)]
    wave2 = synthesizer.generate_chord(chord, 1.0)
    chord = [BASE,  BASE * 2.0 ** (4 / 12.0), BASE * 2.0 ** (7 / 12.0), BASE * 2.0 ** (12 / 12.0)]
    wave3 = synthesizer.generate_chord(chord, 1.0)

    writer.write_waves(os.path.join(DIR, "test.wav"), wave1, wave2, wave3)


if __name__ == '__main__':
    main()

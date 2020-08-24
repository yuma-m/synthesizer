# In this demo, the chords passed as arguments will be played.

import argparse

from pychord import ChordProgression

from synthesizer import Player, Synthesizer, Waveform


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("chord", nargs="+", help="The chord to be played")
    return parser.parse_args()


def main():
    args = parse_args()
    chords = ChordProgression(args.chord)

    player = Player()
    player.open_stream()
    synthesizer = Synthesizer(osc1_waveform=Waveform.triangle, osc1_volume=1.0, use_osc2=False)

    for chord in chords:
        notes = chord.components_with_pitch(root_pitch=3)
        print("Play {}".format(chord))
        player.play_wave(synthesizer.generate_chord(notes, 1.0))


if __name__ == '__main__':
    main()

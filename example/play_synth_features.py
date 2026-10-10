#!/usr/bin/env python3

import time

from synthesizer import FilterType, Player, Synthesizer, Waveform

PRESETS = {
    "detuned saw pad": dict(
        osc1_waveform=Waveform.sawtooth, use_osc2=True, osc2_waveform=Waveform.sawtooth,
        osc2_volume=1.0, osc2_freq_transpose=1.0, osc2_detune=10.0,
        filter_type=FilterType.lowpass, filter_cutoff=1500.0,
        attack=0.5, release=0.8,
    ),
    "pluck": dict(
        osc1_waveform=Waveform.square, osc1_volume=0.6, osc1_pulse_width=0.3,
        filter_type=FilterType.lowpass, filter_cutoff=2000.0, filter_resonance=2.0,
        attack=0.005, decay=0.4, sustain=0.0, release=0.05,
    ),
    "wah": dict(
        osc1_waveform=Waveform.sawtooth, osc1_volume=0.4,
        filter_type=FilterType.lowpass, filter_cutoff=800.0, filter_resonance=6.0,
        lfo_rate=2.0, lfo_cutoff_depth=2.0,
    ),
    "vibrato and tremolo": dict(
        osc1_waveform=Waveform.triangle,
        lfo_rate=6.0, lfo_pitch_depth=30.0, lfo_amp_depth=0.4,
        attack=0.1, release=0.3,
    ),
    "noise hi-hat": dict(
        osc1_waveform=Waveform.noise,
        filter_type=FilterType.highpass, filter_cutoff=7000.0,
        attack=0.001, decay=0.08, sustain=0.0, release=0.01,
    ),
}


def main():
    player = Player()
    player.open_stream()

    for name, params in PRESETS.items():
        print("play {}".format(name))
        synthesizer = Synthesizer(**params)
        if params["osc1_waveform"] is Waveform.noise:
            for _ in range(8):
                player.play_wave(synthesizer.generate_constant_wave(440.0, 0.25))
        else:
            player.play_wave(synthesizer.generate_chord(["C3", "G3", "Eb4"], 3.0))
        time.sleep(0.5)


if __name__ == '__main__':
    main()

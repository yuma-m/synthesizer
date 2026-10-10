# Python synthesizer ![Build Status](https://github.com/yuma-m/synthesizer/actions/workflows/build.yml/badge.svg) [![Documentation Status](https://readthedocs.org/projects/synthesizer/badge/?version=latest)](http://synthesizer.readthedocs.io/en/latest/?badge=latest)

- Virtual analog synthesizer. 

## Installation

```bash
$ pip install synthesizer
```

To play sounds with `Player`, install [PyAudio](https://pypi.org/project/PyAudio/) as well.

```bash
$ pip install "synthesizer[audio]"
```

### Install dependencies for PyAudio

#### Ubuntu

```bash
$ apt install portaudio19-dev
```

### macOS

```bash
$ brew install portaudio
```

## Basic usage

### Play 440Hz sine wave

```python
>>> from synthesizer import Player, Synthesizer, Waveform


>>> player = Player()
>>> player.open_stream()
>>> synthesizer = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
# Play A4
>>> player.play_wave(synthesizer.generate_constant_wave(440.0, 3.0))
```

### Play chord

```python
# Play C major
>>> chord = ["C3", "E3", "G3"]
>>> player.play_wave(synthesizer.generate_chord(chord, 3.0))

# You can also specify frequencies to play just intonation
>>> chord = [440.0, 550.0, 660.0]
>>> player.play_wave(synthesizer.generate_chord(chord, 3.0))
```

You can use [PyChord](https://github.com/yuma-m/pychord) to handle chords easily.

```python
>>> from pychord import Chord
>>> chord = Chord("Dm7/G")
>>> player.play_wave(synthesizer.generate_chord(chord.components_with_pitch(root_pitch=3), 3.0))
```

### Noise, pulse width and detune

```python
# White noise (pass seed to make it reproducible)
>>> synthesizer = Synthesizer(osc1_waveform=Waveform.noise, seed=42)

# Square wave with 25% duty cycle
>>> synthesizer = Synthesizer(osc1_waveform=Waveform.square, osc1_pulse_width=0.25)

# Detune oscillator 2 by +7 cents for a thicker sound
>>> synthesizer = Synthesizer(osc1_waveform=Waveform.sawtooth, use_osc2=True,
...                           osc2_waveform=Waveform.sawtooth, osc2_volume=1.0,
...                           osc2_freq_transpose=1.0, osc2_detune=7.0)
```

### ADSR envelope

Each generated wave fades in and out (10 ms by default) to prevent click noise between notes.
The release is included in the length of the wave.

```python
>>> synthesizer = Synthesizer(osc1_waveform=Waveform.sine, attack=0.05, release=0.2)
# Disable the envelope
>>> synthesizer = Synthesizer(osc1_waveform=Waveform.sine, attack=0.0, release=0.0)
```

Use `decay` and `sustain` for a full ADSR envelope, e.g. a plucked sound.

```python
>>> synthesizer = Synthesizer(osc1_waveform=Waveform.sawtooth,
...                           attack=0.005, decay=0.3, sustain=0.2, release=0.1)
```

### Filter

A resonant 2-pole (12 dB/oct) filter can be applied to the oscillators.
`filter_resonance` is the Q factor; values above 0.707 emphasize the cutoff frequency.

```python
>>> from synthesizer import FilterType
>>> synthesizer = Synthesizer(osc1_waveform=Waveform.sawtooth,
...                           filter_type=FilterType.lowpass, filter_cutoff=800.0, filter_resonance=4.0)
```

Available filter types are `FilterType.lowpass`, `FilterType.highpass` and `FilterType.bandpass`.
High resonance may push the wave beyond [-1.0, 1.0]; such samples are clipped when played or written.

### Specify audio device

```python
>>> player.enumerate_device()
# index: 00, name: "Built-in Microphone", rate: 44100
# index: 01, name: "Built-in Output", rate: 44100
# index: 02, name: "UA-25EX 44.1kHz", rate: 44100
>>> player.open_stream(device_name="UA-25EX")
```

### Write wav file

```python
>>> from synthesizer import Writer
>>> writer = Writer()

>>> chord = ["C4", "E4", "G4"]
>>> wave = synthesizer.generate_chord(chord, 3.0)
>>> writer.write_wave("path/to/your.wav", wave)
```

## Examples

### play_pychord.py

Play chords using [PyChord](https://github.com/yuma-m/pychord).

```bash
pip install pychord>=0.5.0
python example/play_pychord.py A C#m7 DM7 Bm7/E A
```

## Supported OS

- macOS
- Linux

## Supported versions

- Python 3.10 and above

## Author

- [Yuma Mihira](https://yuma.cloud/)

## License

- MIT License

## Links

- PyPI: <https://pypi.python.org/pypi/synthesizer>
- GitHub: <https://github.com/yuma-m/synthesizer>
- Document: <https://synthesizer.readthedocs.io>

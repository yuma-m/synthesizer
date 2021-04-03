# Python synthesizer ![Build Status](https://github.com/yuma-m/synthesizer/actions/workflows/build.yml/badge.svg) [![Documentation Status](https://readthedocs.org/projects/synthesizer/badge/?version=latest)](http://synthesizer.readthedocs.io/en/latest/?badge=latest)

- Virtual analog synthesizer. 

## Installation

```bash
$ pip install synthesizer
```

### Install dependencies

#### Ubuntu

```bash
$ apt install portaudio19-dev
$ pip install pyaudio
```

### macOS

```bash
$ brew install portaudio
$ pip install pyaudio
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

- macOS 10.12 and above
- Ubuntu 16.04

## Supported versions

- Python 2.7
- Python 3.5 and above

## Author

- [Yuma Mihira](http://yurax2.com/)

## License

- GPL v3 License

## Links

- PyPI: https://pypi.python.org/pypi/synthesizer
- GitHub: https://github.com/yuma-m/synthesizer
- Document: https://synthesizer.readthedocs.io

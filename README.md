# Python synthesizer [![Build Status](https://travis-ci.org/yuma-m/synthesizer.svg?branch=master)](https://travis-ci.org/yuma-m/synthesizer)

- Virtual analog synthesizer. 

## Installation

```bash
$ pip install synthesizer
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
>>> chord = [261.626,  329.628, 391.996]
>>> player.play_wave(synthesizer.generate_chord(chord, 3.0))
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

>>> chord = [261.626,  329.628, 391.996]
>>> wave = synthesizer.generate_chord(chord, 3.0)
>>> writer.write_wave("path/to/your.wav", wave)
```

## Supported OS

- macOS Sierra
- Ubuntu 16.04

## Supported versions

- Python 2.7
- Python 3.4 and above

## Author

- [Yuma Mihira](http://yurax2.com/)

## License

- GPL v3 License

## Links

- PyPI: https://pypi.python.org/pypi/synthesizer
- GitHub: https://github.com/yuma-m/synthesizer

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
>>> from synthesizer import Player, Synthesizer, Waveform

>>> player = Player()
>>> player.open_stream()
>>> synthesizer = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
>>> chord = [261.626,  329.628, 391.996]
# Play C major
>>> player.play_wave(synthesizer.generate_chord(chord, 3.0))
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

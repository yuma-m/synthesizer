# Python synthesizer [![Build Status](https://travis-ci.org/yuma-m/synthesizer.svg?branch=master)](https://travis-ci.org/yuma-m/synthesizer)

- Virtual analog synthesizer. 

## Supported OS

- macOS Sierra
- Ubuntu 16.04

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
>>> player.play_wave(synthesizer.generate_constant_wave(440.0, 3.0))
```


## Author
- [Yuma Mihira](http://yurax2.com/)

## License

- GPL v3 License

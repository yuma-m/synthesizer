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
index: 00, name: "Loopback: PCM (hw:0,0)", rate: 44100.0
index: 01, name: "Loopback: PCM (hw:0,1)", rate: 44100.0
index: 02, name: "HDA Intel PCH: ALC892 Analog (hw:1,0)", rate: 44100.0
index: 03, name: "HDA Intel PCH: ALC892 Alt Analog (hw:1,2)", rate: 44100.0
index: 04, name: "sysdefault", rate: 48000
index: 05, name: "front", rate: 44100
index: 06, name: "default", rate: 44100
>>> player.open_stream(device_name="Loopback: PCM (hw:0,0)")
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

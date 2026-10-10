# Changelog

## 0.3.0

- Support Python 3.10 and above, and drop support for Python 2.7 and Python 3.9 and below.
- Remove `enum34` dependency.
- `PyAudio` can be installed as an optional dependency with `pip install "synthesizer[audio]"`.
- `frequency_from_scale()` raises `ValueError` for unknown notes instead of returning it.
- Migrate packaging to `pyproject.toml` and tests from nose to pytest.
- Add example to integrate with [PyChord](https://github.com/yuma-m/pychord).

## 0.2.0

- Support scale expression to generate chord.

## 0.1.5

- Support triangle wave.
    - Contributor: @AntiMatterAMA

## 0.1.4

- Fix channels of Player class from 2 to 1 to play proper sound.

## 0.1.3

- Specify audio output device.
- Add Writer class.

## 0.1.2

- Add generate_chord method.

## 0.1.1

- Add Synthesizer and Player classes.
- Generate and play constant frequency wave.

## 0.1.0

- Initial version.

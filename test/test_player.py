# -*- coding: utf-8 -*-

import numpy as np
import pytest

from synthesizer import Player


def test_enumerate_device_without_pyaudio(no_pyaudio):
    with pytest.raises(ImportError):
        Player().enumerate_device()


def test_open_stream_without_pyaudio(no_pyaudio):
    with pytest.raises(ImportError):
        Player().open_stream()


def test_enumerate_device(fake_pyaudio, capsys):
    Player().enumerate_device()
    assert capsys.readouterr().out.splitlines() == [
        'index: 00, name: "Built-in Microphone", rate: 44100',
        'index: 01, name: "Built-in Output", rate: 44100',
        'index: 02, name: "UA-25EX 44.1kHz", rate: 48000',
    ]


def test_open_default_stream(fake_pyaudio):
    player = Player()
    player.open_stream()
    assert player._stream.kwargs == {
        "channels": 1,
        "format": fake_pyaudio.paInt16,
        "rate": 44100,
        "output_device_index": 1,
        "output": True,
    }


def test_open_stream_with_rate(fake_pyaudio):
    player = Player(rate=16000)
    player.open_stream()
    assert player._stream.kwargs["rate"] == 16000


def test_open_stream_by_device_name(fake_pyaudio):
    player = Player()
    player.open_stream(device_name="UA-25EX")
    assert player._stream.kwargs["output_device_index"] == 2


def test_open_stream_by_device_index(fake_pyaudio):
    player = Player()
    player.open_stream(device_index=0)
    assert player._stream.kwargs["output_device_index"] == 0


def test_open_stream_device_name_takes_precedence(fake_pyaudio):
    player = Player()
    player.open_stream(device_name="Microphone", device_index=2)
    assert player._stream.kwargs["output_device_index"] == 0


def test_open_stream_unknown_device_name(fake_pyaudio):
    with pytest.raises(RuntimeError):
        Player().open_stream(device_name="Unknown Device")


def test_play_wave_without_stream(fake_pyaudio):
    with pytest.raises(RuntimeError):
        Player().play_wave(np.zeros(10))


def test_play_wave(fake_pyaudio):
    player = Player()
    player.open_stream()
    wave = np.array([1.0, -1.0, 0.0, 0.5])
    player.play_wave(wave)
    assert player._stream.written == [
        np.array([32767, -32767, 0, 16383], dtype=np.int16).tobytes(),
    ]

# -*- coding: utf-8 -*-

import sys
import types

import pytest


class FakeStream(object):

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.written = []

    def write(self, data):
        self.written.append(data)


class FakePyAudio(object):

    devices = [
        {"index": 0, "name": "Built-in Microphone", "defaultSampleRate": 44100.0},
        {"index": 1, "name": "Built-in Output", "defaultSampleRate": 44100.0},
        {"index": 2, "name": "UA-25EX 44.1kHz", "defaultSampleRate": 48000.0},
    ]
    default_output_index = 1

    def __init__(self):
        self.stream = None

    def get_device_count(self):
        return len(self.devices)

    def get_device_info_by_index(self, index):
        return self.devices[index]

    def get_default_output_device_info(self):
        return self.devices[self.default_output_index]

    def open(self, **kwargs):
        self.stream = FakeStream(**kwargs)
        return self.stream


@pytest.fixture
def fake_pyaudio(monkeypatch):
    module = types.ModuleType("pyaudio")
    module.PyAudio = FakePyAudio
    module.paInt16 = 8
    monkeypatch.setitem(sys.modules, "pyaudio", module)
    return module


@pytest.fixture
def no_pyaudio(monkeypatch):
    # A None entry in sys.modules makes `import pyaudio` raise ImportError
    monkeypatch.setitem(sys.modules, "pyaudio", None)

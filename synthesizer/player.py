# -*- coding: utf-8 -*-

import struct

import pyaudio
import numpy as np


class Player(object):

    def __init__(self, channels=2, rate=44100):
        self._pyaudio = pyaudio.PyAudio()
        self._stream = None
        self._channels = channels
        self._rate = rate

    def open_stream(self):
        default_device = self._pyaudio.get_default_output_device_info()

        self._stream = self._pyaudio.open(
            channels=self._channels,
            format=pyaudio.paInt16,
            rate=self._rate,
            output_device_index=default_device["index"],
            output=True,
        )

    def play_wave(self, wave):
        if not self._stream:
            raise RuntimeError("audio stream is not opened, please call open_stream() first.")
        wave = (wave * float(2 ** 15 - 1)).astype(np.int16).tolist()
        data = struct.pack("h" * len(wave), *wave)
        self._stream.write(data)

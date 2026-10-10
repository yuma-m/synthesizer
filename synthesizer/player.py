from .utils import to_int16


class Player:

    def __init__(self, rate=44100):
        try:
            import pyaudio
            self._pyaudio = pyaudio.PyAudio()
            self._format = pyaudio.paInt16
        except ImportError:
            self._pyaudio = None
        self._stream = None
        # TODO: support stereo channels
        self._channels = 1
        self._rate = rate

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def enumerate_device(self):
        if not self._pyaudio:
            raise ImportError("Failed to import pyaudio, please install pyaudio")
        for n in range(self._pyaudio.get_device_count()):
            device = self._pyaudio.get_device_info_by_index(n)
            print('index: {index:02d}, name: "{name}", rate: {rate:5d}'.format(
                index=n, name=device["name"], rate=int(device["defaultSampleRate"])))

    def open_stream(self, device_name=None, device_index=-1):
        """ open audio output stream

        if neither device_name nor device_index is specified,
        default output device will be opened.

        devices without output channels (e.g. microphones) are ignored
        when searching by device_name.

        :param str device_name: part of device name (ex: hw:0,0)
        :param int device_index: index of device
        """
        if not self._pyaudio:
            raise ImportError("Failed to import pyaudio, please install pyaudio")
        if device_name:
            for n in range(self._pyaudio.get_device_count()):
                dev = self._pyaudio.get_device_info_by_index(n)
                if dev["name"].find(device_name) >= 0 and dev["maxOutputChannels"] > 0:
                    device = dev
                    break
            else:
                raise RuntimeError("audio output device {} not found".format(device_name))
        elif device_index >= 0:
            device = self._pyaudio.get_device_info_by_index(device_index)
            if device["maxOutputChannels"] <= 0:
                raise RuntimeError("audio device {} ({}) has no output channels".format(
                    device_index, device["name"]))
        else:
            device = self._pyaudio.get_default_output_device_info()

        self.close_stream()
        self._stream = self._pyaudio.open(
            channels=self._channels,
            format=self._format,
            rate=self._rate,
            output_device_index=device["index"],
            output=True,
        )

    def play_wave(self, wave):
        """ play normalized wave

        :param numpy.array wave: normalized wave
        """
        if not self._stream:
            raise RuntimeError("audio stream is not opened, please call open_stream() first.")
        self._stream.write(to_int16(wave).tobytes())

    def close_stream(self):
        """ close audio output stream if opened """
        if self._stream:
            try:
                self._stream.stop_stream()
                self._stream.close()
            except OSError:
                # PyAudio may have already closed the stream after an I/O error
                pass
            finally:
                self._stream = None

    def close(self):
        """ close audio output stream and release PyAudio resources """
        self.close_stream()
        if self._pyaudio:
            self._pyaudio.terminate()
            self._pyaudio = None

import numpy as np
import pytest
from scipy.io import wavfile

from synthesizer import Synthesizer, Waveform, Writer


def _to_int16(wave):
    return (wave * (2 ** 15 - 1)).astype(np.int16)


@pytest.mark.parametrize("rate", [44100, 16000])
def test_write_wave(tmp_path, rate):
    path = tmp_path / "test_wave.wav"
    writer = Writer(rate=rate)
    synthesizer = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False, rate=rate)
    wave = synthesizer.generate_constant_wave(440.0, 1.0)

    writer.write_wave(str(path), wave)

    read_rate, data = wavfile.read(str(path))
    assert read_rate == rate
    assert data.dtype == np.int16
    np.testing.assert_array_equal(data, _to_int16(wave))


def test_write_wave_default_rate(tmp_path):
    path = tmp_path / "test_wave.wav"
    Writer().write_wave(str(path), np.zeros(10))
    read_rate, _ = wavfile.read(str(path))
    assert read_rate == 44100


def test_write_wave_full_scale(tmp_path):
    path = tmp_path / "test_wave.wav"
    Writer().write_wave(str(path), np.array([1.0, -1.0, 0.0, 0.5]))
    _, data = wavfile.read(str(path))
    np.testing.assert_array_equal(data, np.array([32767, -32767, 0, 16383], dtype=np.int16))


def test_write_wave_clips_out_of_range(tmp_path):
    path = tmp_path / "test_wave.wav"
    Writer().write_wave(str(path), np.array([1.5, -1.5]))
    _, data = wavfile.read(str(path))
    np.testing.assert_array_equal(data, np.array([32767, -32767], dtype=np.int16))


def test_write_waves(tmp_path):
    path = tmp_path / "test_waves.wav"
    writer = Writer()
    synthesizer = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
    wave1 = synthesizer.generate_constant_wave(220.0, 1.0)
    wave2 = synthesizer.generate_constant_wave(440.0, 0.5)

    writer.write_waves(str(path), wave1, wave2)

    read_rate, data = wavfile.read(str(path))
    assert read_rate == 44100
    assert data.size == wave1.size + wave2.size
    np.testing.assert_array_equal(data, _to_int16(np.concatenate([wave1, wave2])))

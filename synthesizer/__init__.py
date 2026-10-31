from importlib.metadata import PackageNotFoundError, version

from .filter import Filter, FilterType
from .player import Player
from .synthesizer import Oscillator, Synthesizer, Waveform
from .writer import Writer

try:
    __version__ = version("synthesizer")
except PackageNotFoundError:  # pragma: no cover - not installed, e.g. running from a source tree
    __version__ = "0.0.0"

__all__ = [
    "Filter",
    "FilterType",
    "Oscillator",
    "Player",
    "Synthesizer",
    "Waveform",
    "Writer",
    "__version__",
]

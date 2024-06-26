# pylint: disable='missing-module-docstring'
from .download_resources import *


try:
    import importlib.metadata as importlib_metadata

except ModuleNotFoundError:
    import importlib_metadata  # type: ignore


try:
    __version__ = importlib_metadata.version(__name__)

except importlib_metadata.PackageNotFoundError:
    __version__ = "1.2.9"

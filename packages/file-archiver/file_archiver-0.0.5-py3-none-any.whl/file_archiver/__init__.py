import importlib

__version__ = importlib.metadata.version("file_archiver")

from file_archiver.archive import Archive

__all__ = ["Archive"]

# Version is derived from git tags by setuptools-scm at build-time.
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("pythontemplate")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = []

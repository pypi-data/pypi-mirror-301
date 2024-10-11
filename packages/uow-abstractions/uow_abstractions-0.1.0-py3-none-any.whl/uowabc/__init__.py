from importlib.metadata import PackageNotFoundError, version

from uowabc.base import BaseRepository, TExc, TUow, UnitOfWork  # noqa: F401

try:
    __version__ = version('uow')

except PackageNotFoundError:
    __version__ = '0.0.0'

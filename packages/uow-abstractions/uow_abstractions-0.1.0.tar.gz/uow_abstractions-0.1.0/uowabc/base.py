from __future__ import annotations

import asyncio
import logging
from typing import Any, Generic, Literal, Self, TypeVar

TExc = TypeVar('TExc', bound=BaseException)

logger = logging.getLogger('uow')


class UnitOfWork(object):
    """Manage the lifecycle of a unit of work.

    This class is designed to be used with asynchronous context managers (`async with`),
    ensuring that resources are properly initialized and cleaned up. Extend this
    class to implement specific resource management strategies (e.g., for databases, transactions).

    Example usage:

    async def some_func():
        async with CustomUnitOfWork() as uow:
            # Perform operations within the unit of work
            pass

    Methods:
        - aenter(): Custom initialization logic (to be overridden).
        - aexit(): Custom cleanup logic (to be overridden).

    """

    def __init__(self) -> None:
        """Initialize the UnitOfWork object."""
        pass

    async def __aenter__(self) -> Self:
        """Enter the context of the unit of work asynchronously."""
        await self.aenter()
        return self

    async def __aexit__(self, *args, **kwargs) -> bool:
        """Exit the context of the unit of work asynchronously, ensuring resources are cleaned up."""
        await self.aexit(*args, **kwargs)
        return False

    async def aenter(self):
        """Run custom logic when entering the unit of work (to be overridden)."""
        pass

    async def aexit(self, exc_type: type[TExc] | None, exc: TExc | None, traceback: Any | None):
        """Run custom logic when exiting the unit of work (to be overridden)."""
        pass

    def __dell__(self):
        """Ensure the resources are cleaned up when the object is deleted."""
        asyncio.run(self.aexit(None, None, None))


TUow = TypeVar('TUow', bound=UnitOfWork)


class BaseRepository(Generic[TUow]):
    """Provide a base repository for interacting with the database.

    This class provides an interface for repositories that require
    a unit of work to manage transactions or resources.

    Example usage:

    def func():
        async with AdvertRepository() as advert_repository:
            await advert_repository.add_one(...)

    def func():
        uow = UnitOfWork()
        async with AdvertRepository(uow) as advert_repository:
            await advert_repository.add_one(...)

    def func():
        async with UnitOfWork() as uow:
            await AdvertRepository(uow).add_one(...)

    Methods:
        - aenter(): Custom initialization logic (to be overridden).
        - aexit(): Custom cleanup logic (to be overridden).

    """

    UowType: type[TUow]
    uow: TUow

    def __init__(self, uow: TUow | None = None, **kwargs: Any) -> None:
        """Initialize the repository with the provided unit of work or create a new one."""
        self.uow = uow or self.UowType(**kwargs)

    async def __aenter__(self) -> Self:
        """Enter the context of both the repository and its unit of work asynchronously."""
        await self.uow.aenter()
        await self.aenter()
        return self

    async def __aexit__(self, *args: Any, **kwargs: Any) -> Literal[False]:
        """Exit the context of both the repository and its unit of work asynchronously."""
        await self.aexit(*args, **kwargs)
        await self.uow.aexit(*args, **kwargs)
        return False

    async def aenter(self):
        """Run custom logic for initializing the repository (to be overridden)."""
        pass

    async def aexit(self, exc_type: type[TExc] | None, exc: TExc | None, traceback: Any | None):
        """Run custom logic for cleaning up the repository (to be overridden)."""
        pass

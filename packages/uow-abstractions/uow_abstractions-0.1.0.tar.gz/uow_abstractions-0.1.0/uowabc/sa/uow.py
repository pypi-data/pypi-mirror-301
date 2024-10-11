from __future__ import annotations

import asyncio
import logging
import typing

import uowabc

TExc = typing.TypeVar('TExc', bound=BaseException)

if typing.TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any

    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


logger = logging.getLogger('uow')


class SaSessionUnitOfWork(uowabc.UnitOfWork):
    session: AsyncSession | None
    session_factory: Callable[[], AsyncSession] | None
    lock: asyncio.Lock | None

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        lock: asyncio.Lock | None = None,
    ) -> None:
        super().__init__()
        self.session = None
        self.session_factory = session_factory
        self.lock = lock

    async def aenter(self):
        await super().aenter()

        if self.lock is not None:
            await self.lock.acquire()

        await self.make_session()

    async def aexit(self, exc_type: type[TExc] | None, exc: TExc | None, traceback: Any | None):
        assert self.session is not None

        if exc is None:
            await self.commit()

        else:
            logger.exception(exc)
            await self.rollback()

        await self.close()

        if self.lock is not None:
            self.lock.release()

        await super().aexit(exc_type, exc, traceback)

    async def make_session(self) -> None:
        assert self.session is None
        assert self.session_factory is not None

        self.session = self.session_factory()

    async def commit(self) -> None:
        assert self.session is not None
        await self.session.commit()

    async def rollback(self) -> None:
        assert self.session is not None
        await self.session.rollback()

    async def close(self) -> None:
        assert self.session is not None

        await self.session.close()
        self.session = None

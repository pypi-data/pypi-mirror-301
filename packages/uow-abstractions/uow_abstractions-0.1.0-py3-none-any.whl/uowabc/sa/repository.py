from __future__ import annotations

import asyncio
import logging
from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.decl_api import DeclarativeBase

import uowabc
from uowabc.sa.mixins import CrudMixin
from uowabc.sa.uow import SaSessionUnitOfWork

TBase = TypeVar('TBase', bound=DeclarativeBase)
TSaUow = TypeVar('TSaUow', bound=SaSessionUnitOfWork)

logger = logging.getLogger('rocshers_sdk')


class SaSessionRepository(uowabc.BaseRepository[TSaUow]):
    UowType = SaSessionUnitOfWork  # type: ignore
    uow: TSaUow
    lock: asyncio.Lock

    @property
    def session(self) -> AsyncSession:
        assert isinstance(self.uow.session, AsyncSession)
        return self.uow.session


class CrudSaSessionRepository(SaSessionRepository[TSaUow], CrudMixin[TBase]):
    UowType = SaSessionUnitOfWork  # type: ignore
    model: type[TBase]

from __future__ import annotations

import logging
from typing import Any, Generic, TypeVar
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.decl_api import DeclarativeBase

from uowabc.sa.uow import SaSessionUnitOfWork

TBase = TypeVar('TBase', bound=DeclarativeBase)
TSaUow = TypeVar('TSaUow', bound=SaSessionUnitOfWork)

logger = logging.getLogger('uow')


class CrudMixin(Generic[TBase]):
    model: type[TBase]

    @property
    def session(self) -> AsyncSession:
        raise NotImplementedError()

    async def create(self, fields: dict[str, Any]) -> TBase:
        stmt = sa.insert(self.model).values(**fields).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get(self, **filter_by: Any) -> list[TBase]:
        stmt = sa.select(self.model)

        if filter_by:
            stmt = stmt.filter_by(**filter_by)

        res = await self.session.execute(stmt)
        return [row[0] for row in res.all()]

    async def get_one(self, **filter_by: Any) -> TBase | None:
        stmt = sa.select(self.model)

        if filter_by:
            stmt = stmt.filter_by(**filter_by)

        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def update(self, filter_by: dict[str, Any], data: dict[str, Any]) -> int:
        stmt = sa.update(self.model).values(**data)
        stmt = stmt.filter_by(**filter_by)
        result = await self.session.execute(stmt)
        return result.rowcount

    async def update_one(self, pk: UUID | int, data: dict[str, Any]) -> TBase:
        stmt = sa.update(self.model).filter_by(pk=pk).values(**data).returning(self.model)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()

    async def delete(self, **filter_by: Any) -> int:
        stmt = sa.delete(self.model)
        stmt = stmt.filter_by(**filter_by)
        result = await self.session.execute(stmt)
        return result.rowcount

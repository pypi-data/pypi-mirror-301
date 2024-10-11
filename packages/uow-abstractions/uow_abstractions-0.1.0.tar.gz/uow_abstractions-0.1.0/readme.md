# Unit Of Work Abstractions

[![PyPI](https://img.shields.io/pypi/v/uow-abstractions)](https://pypi.org/project/uow-abstractions/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/uow-abstractions)](https://pypi.org/project/uow-abstractions/)
[![GitLab last commit](https://img.shields.io/gitlab/last-commit/rocshers/python/uow-abstractions)](https://gitlab.com/rocshers/python/uow-abstractions)

[![Homepage](https://img.shields.io/badge/Homepage-orange)](https://projects.rocshers.com/open-source/uow-abstractions)
[![Downloads](https://static.pepy.tech/badge/uow-abstractions)](https://pepy.tech/project/uow-abstractions)
[![GitLab stars](https://img.shields.io/gitlab/stars/rocshers/python/uow-abstractions)](https://gitlab.com/rocshers/python/uow-abstractions)

## Classes

## Instruction

### SqlAlchemy

This package provides a small abstraction layer over the UOW (Unit of Work) pattern for working with `sqlalchemy`.

- `uowabc.sa.SaSessionUnitOfWork` – A class that contains an `async_sessionmaker[AsyncSession]` and automatically calls `.commit` or `.rollback` when the context is closed.
- `uowabc.sa.SaSessionRepository` – A base repository containing an `AsyncSession`, extending the functionality of `SaSessionUnitOfWork`.
- `uowabc.sa.CrudSaSessionRepository` – A repository based on `SaSessionRepository`, designed to work with `DeclarativeBase` and implements basic `CRUD` methods.

```python

import uowabc.sa
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


class Row(DeclarativeBase):
    __tablename__ = 'rows'

    id = Column(Integer, primary_key=True, autoincrement=True)


# First step - Declaring the UOW

engine = create_async_engine('...')
session_maker = async_sessionmaker(engine, expire_on_commit=False)

class DatabaseSaUow(uowabc.sa.SaSessionUnitOfWork):
    def __init__(self) -> None:
        super().__init__(session_maker)

# Second step - Defining the repository

class RowsRepository(uowabc.sa.CrudSaSessionRepository[DatabaseSaUow, Row]):
    UowType = DatabaseSaUow
    model = Row

    async def get_row_count(self) -> int:
        result = await self.session.execute(select(func.count()).select_from(self.model))
        count = result.scalar_one()
        return count

# Step three - Execution

async def example_1():
    # Sequentially create the UOW and the repository

    async with DatabaseSaUow() as uow:
        async with RowsRepository(uow) as rows_repository:
            await rows_repository.get_row_count()

async def example_2(uow: DatabaseSaUow):
    # Initialize the repository by passing an already created UOW
    # The UOW must be "started" (the context manager must be invoked)

    async with RowsRepository(uow) as rows_repository:
        await rows_repository.get_row_count()

async def example_3():
    # Initialize the repository without a pre-created UOW
    # The UOW will be automatically created

    async with RowsRepository() as rows_repository:
        await rows_repository.get_row_count()
```

## Dependencies

This module uses types introduced in `python 3.12`

## Contribute

Issue Tracker: <https://gitlab.com/rocshers/python/uow-abstractions/-/issues>  
Source Code: <https://gitlab.com/rocshers/python/uow-abstractions>

Before adding changes:

```bash
make install-dev
```

After changes:

```bash
make format test
```

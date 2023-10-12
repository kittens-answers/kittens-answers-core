from collections.abc import AsyncGenerator, Callable

import pytest
from mimesis import Field

from kittens_answers_core.models import User
from kittens_answers_core.services.base import BaseUnitOfWork
from kittens_answers_core.services.db import SQLAlchemyUnitOfWork
from kittens_answers_core.services.db.models import Base
from kittens_answers_core.services.memory import MemoryUnitOfWork


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    if uow.__name__ in metafunc.fixturenames:
        metafunc.parametrize(uow.__name__, [MemoryUnitOfWork, SQLAlchemyUnitOfWork], indirect=True)


@pytest.fixture
async def uow(db_container_url: str, request: pytest.FixtureRequest) -> AsyncGenerator[BaseUnitOfWork, None]:
    if request.param == MemoryUnitOfWork:
        yield MemoryUnitOfWork()
    elif request.param == SQLAlchemyUnitOfWork:
        _uow = SQLAlchemyUnitOfWork(db_url=db_container_url)
        async with _uow._engine.begin() as connection:  # pyright: ignore [reportPrivateUsage]
            await connection.run_sync(Base.metadata.create_all)
        yield _uow
        async with _uow._engine.begin() as connection:  # pyright: ignore [reportPrivateUsage]
            await connection.run_sync(Base.metadata.drop_all)
    else:
        msg = "invalid uow type in test config"
        raise ValueError(msg)


@pytest.fixture
def user_foreign_id_factory() -> Callable[..., str]:
    field = Field()

    def _user_foreign_id_factory() -> str:
        return field("increment", key=str)

    return _user_foreign_id_factory


@pytest.fixture
def user_uid_factory() -> Callable[..., str]:
    field = Field()

    def _user_uid_factory() -> str:
        return field("uuid")

    return _user_uid_factory


@pytest.fixture
async def populate_users(uow: BaseUnitOfWork, user_foreign_id_factory: Callable[..., str]) -> list[User]:
    result: list[User] = []
    async with uow:
        for _ in range(4):
            user = await uow.user_services.create(foreign_id=user_foreign_id_factory())
            result.append(user)
        await uow.commit()
    return result

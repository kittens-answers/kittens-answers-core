from collections.abc import AsyncGenerator, Callable
from uuid import UUID

import pytest
from mimesis import Field, Schema
from mimesis.keys import maybe
from mimesis.types import JSON

from kittens_answers_core.models import Question, QuestionTypes, User
from kittens_answers_core.services.base.uow import BaseUnitOfWork
from kittens_answers_core.services.db.models import Base
from kittens_answers_core.services.db.uow import SQLAlchemyUnitOfWork
from kittens_answers_core.services.memory.uow import MemoryUnitOfWork


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    uow_list = [
        MemoryUnitOfWork,
        SQLAlchemyUnitOfWork,
    ]
    if uow.__name__ in metafunc.fixturenames:
        metafunc.parametrize(uow.__name__, uow_list, indirect=True)


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
def user_uid_factory() -> Callable[..., UUID]:
    field = Field()

    def _user_uid_factory() -> UUID:
        return field("uuid_object")

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


@pytest.fixture
def question_uid_factory() -> Callable[..., UUID]:
    field = Field()

    def _question_uid_factory() -> UUID:
        return field("uuid_object")

    return _question_uid_factory


@pytest.fixture
def question_data_factory() -> Callable[..., JSON]:
    field = Field()
    schema = Schema(
        schema=lambda: {
            "question_type": (question_type := field("random.choice_enum_item", enum=QuestionTypes)),
            "question_text": field("sentence"),
            "options": set(field("words", key=maybe([], probability=0.2))),
            "extra_options": set(field("words", key=maybe([], probability=0.2)))
            if question_type == QuestionTypes.MATCH
            else set(),
        },
        iterations=1,
    )
    data: list[JSON] = []

    def _question_data_factory() -> JSON:
        while True:
            _schema = schema.create()[0]
            if _schema not in data:
                break
        data.append(_schema)
        return _schema

    return _question_data_factory


@pytest.fixture
def random_user_from_db(populate_users: list[User]) -> Callable[..., User]:
    field = Field()

    def _random_user_from_db() -> User:
        return field("random.choice", seq=populate_users)

    return _random_user_from_db


@pytest.fixture
async def populate_questions(
    uow: BaseUnitOfWork, question_data_factory: Callable[..., JSON], random_user_from_db: Callable[..., User]
) -> list[Question]:
    result: list[Question] = []
    async with uow:
        for _ in range(10):
            question = await uow.question_services.create(
                creator_id=random_user_from_db().uid, **question_data_factory()
            )
            result.append(question)
        await uow.commit()
    return result

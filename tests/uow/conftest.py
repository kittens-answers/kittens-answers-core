from collections.abc import AsyncGenerator
from uuid import UUID

import pytest
from mimesis import Field
from mimesis.keys import maybe

from kittens_answers_core.models import Answer, Question, QuestionTypes, User
from kittens_answers_core.services.db.models import Base
from kittens_answers_core.services.db.uow import SQLAlchemyUnitOfWork
from kittens_answers_core.services.memory.uow import MemoryUnitOfWork
from tests.uow.fixture_types import (
    AnswerDataDict,
    AnswerDataFactory,
    AnswerFactory,
    QuestionDataDict,
    QuestionDataFactory,
    QuestionFactory,
    UIDFactory,
    UOWTypes,
    UserDataDict,
    UserDataFactory,
    UserFactory,
)
from tests.uow.providers import AnswerProvider


@pytest.fixture
def mimesis_field() -> Field:
    return Field(providers=[AnswerProvider])


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    uow_list = [
        MemoryUnitOfWork,
        SQLAlchemyUnitOfWork,
    ]
    if uow.__name__ in metafunc.fixturenames:
        metafunc.parametrize(uow.__name__, uow_list, indirect=True)


@pytest.fixture
async def uow(db_container_url: str, request: pytest.FixtureRequest) -> AsyncGenerator[UOWTypes, None]:
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
def user_data_factory(mimesis_field: Field) -> UserDataFactory:
    return lambda: UserDataDict(foreign_id=mimesis_field("increment", key=str))


@pytest.fixture
def uid_factory(mimesis_field: Field) -> UIDFactory:
    return lambda: mimesis_field("uuid_object")


@pytest.fixture
def user_factory(uow: UOWTypes, user_data_factory: UserDataFactory) -> UserFactory:
    async def _user_factory(foreign_id: str | None = None) -> User:
        if foreign_id is None:
            foreign_id = user_data_factory()["foreign_id"]
        async with uow:
            user = await uow.user_services.create(foreign_id=foreign_id)
            await uow.commit()
        return user

    return _user_factory


@pytest.fixture
def question_data_factory(mimesis_field: Field) -> QuestionDataFactory:
    def _question_data_factory(
        question_type: QuestionTypes | None = None, empty_options: bool | None = None
    ) -> QuestionDataDict:
        if empty_options is None:
            probability = 0.2
        elif empty_options is False:
            probability = 0
        else:
            probability = 1
        return QuestionDataDict(
            question_type=(_question_type := mimesis_field("QA.question_type", question_type=question_type)),
            question_text=mimesis_field("sentence"),
            options=mimesis_field("QA.options", key=maybe(set(), probability=probability)),
            extra_options=mimesis_field(
                "QA.extra_options", key=maybe(set(), probability=probability), question_type=_question_type
            ),
        )

    return _question_data_factory


@pytest.fixture
def question_factory(
    uow: UOWTypes, question_data_factory: QuestionDataFactory, user_factory: UserFactory
) -> QuestionFactory:
    async def _question_factory(
        question_data: QuestionDataDict | None = None, user_uid: UUID | None = None
    ) -> Question:
        if user_uid is None:
            user_uid = (await user_factory()).uid
        if question_data is None:
            question_data = question_data_factory()
        async with uow:
            question = await uow.question_services.create(creator_id=user_uid, **question_data)
            await uow.commit()
        return question

    return _question_factory


@pytest.fixture
def answer_data_factory(mimesis_field: Field) -> AnswerDataFactory:
    def _answer_data_factory(question: Question) -> AnswerDataDict:
        return AnswerDataDict(
            answer=mimesis_field("QA.answer", question=question),
            extra_answer=mimesis_field("QA.extra_answer", question=question),
            is_correct=mimesis_field("QA.is_correct"),
            question_uid=question.uid,
        )

    return _answer_data_factory


@pytest.fixture
async def answer_factory(
    uow: UOWTypes,
    question_factory: QuestionFactory,
    answer_data_factory: AnswerDataFactory,
    user_factory: UserFactory,
) -> AnswerFactory:
    async def _answer_factory(
        answer_data: AnswerDataDict | None = None,
        question: Question | None = None,
        user_uid: UUID | None = None,
    ) -> Answer:
        if user_uid is None:
            user_uid = (await user_factory()).uid
        if question is None:
            question = await question_factory(user_uid=user_uid)
        if answer_data is None:
            answer_data = answer_data_factory(question)
        async with uow:
            answer = await uow.answer_services.create(creator_id=user_uid, **answer_data)
            await uow.commit()
        return answer

    return _answer_factory


@pytest.fixture(autouse=True)
async def populate_answers(uow: UOWTypes, answer_factory: AnswerFactory) -> None:
    if isinstance(uow, MemoryUnitOfWork):
        for _ in range(10):
            await answer_factory()

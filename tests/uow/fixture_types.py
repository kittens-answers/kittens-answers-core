from collections.abc import Callable
from typing import Protocol, TypeAlias, TypedDict
from uuid import UUID

from kittens_answers_core.models import Answer, Question, QuestionTypes, User
from kittens_answers_core.uow.db import SQLAlchemyUnitOfWork
from kittens_answers_core.uow.memory import MemoryUnitOfWork

UOWTypes: TypeAlias = MemoryUnitOfWork | SQLAlchemyUnitOfWork


class UserDataDict(TypedDict):
    foreign_id: str


class QuestionDataDict(TypedDict):
    question_type: QuestionTypes
    question_text: str
    options: set[str]
    extra_options: set[str]


class AnswerDataDict(TypedDict):
    answer: list[str]
    extra_answer: list[str]
    is_correct: bool
    question_uid: UUID


UserDataFactory: TypeAlias = Callable[..., UserDataDict]
UIDFactory: TypeAlias = Callable[..., UUID]
QuestionDataFactory: TypeAlias = Callable[..., QuestionDataDict]
AnswerDataFactory: TypeAlias = Callable[[Question], AnswerDataDict]


class QuestionFactory(Protocol):  # pragma: no cover
    @staticmethod
    async def __call__(question_data: QuestionDataDict | None = None, user_uid: UUID | None = None) -> Question:
        ...


class UserFactory(Protocol):  # pragma: no cover
    @staticmethod
    async def __call__(foreign_id: str | None = None) -> User:
        ...


class AnswerFactory(Protocol):  # pragma: no cover
    @staticmethod
    async def __call__(
        answer_data: AnswerDataDict | None = None,
        question: Question | None = None,
        user_uid: UUID | None = None,
    ) -> Answer:
        ...

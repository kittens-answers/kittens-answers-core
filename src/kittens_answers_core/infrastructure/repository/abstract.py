import abc
from typing import Mapping

from kittens_answers_core.domain.entities import (
    Answer,
    IDType,
    Mark,
    Question,
    QuestionType,
    User,
)


class AbstractUserRepository(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    async def create(self, public_id: str) -> User:
        ...

    @abc.abstractmethod
    async def get_by_public_id(self, public_id: str) -> User:
        ...

    @abc.abstractmethod
    async def get_by_id(self, user_id: IDType) -> User:
        ...

    @abc.abstractmethod
    async def list(self) -> tuple[User, ...]:
        ...


class AbstractQuestionRepository(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    async def get_by_id(self, question_id: IDType) -> Question:
        ...

    @abc.abstractmethod
    async def list(self) -> tuple[Question, ...]:
        ...

    @abc.abstractmethod
    async def create(
        self,
        user_id: IDType,
        question_text: str,
        question_type: QuestionType,
        options: frozenset[str],
        extra_options: frozenset[str],
    ) -> Question:
        ...

    @abc.abstractmethod
    async def get(
        self,
        question_text: str,
        question_type: QuestionType,
        options: frozenset[str],
        extra_options: frozenset[str],
    ) -> Question:
        ...


class AbstractAnswerRepository(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    async def create_answer(
        self, user_id: IDType, question_id: IDType, value: str | frozenset[str] | tuple[str, ...] | Mapping[str, str]
    ) -> Answer:
        ...

    @abc.abstractmethod
    async def get_answer(
        self, question_id: IDType, value: str | frozenset[str] | tuple[str, ...] | Mapping[str, str]
    ) -> Answer:
        ...


class AbstractMarkRepository(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    async def create(self, user_id: IDType, answer_id: IDType, value: bool) -> Mark:
        ...

    @abc.abstractmethod
    async def update(self, user_id: IDType, answer_id: IDType, value: bool) -> Mark:
        ...

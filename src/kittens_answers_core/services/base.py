import abc
from types import TracebackType
from typing import Self
from uuid import UUID

from kittens_answers_core.models import Question, QuestionTypes, User


class BaseUserServices(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    async def get_by_foreign_id(self, foreign_id: str) -> User:
        ...

    @abc.abstractmethod
    async def get_by_uid(self, uid: UUID) -> User:
        ...

    @abc.abstractmethod
    async def create(self, foreign_id: str) -> User:
        ...


class BaseQuestionServices(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    async def get_by_uid(self, uid: UUID) -> Question:
        ...

    @abc.abstractmethod
    async def get(
        self,
        question_type: QuestionTypes,
        question_text: str,
        options: set[str],
        extra_options: set[str],
    ) -> Question:
        ...

    @abc.abstractmethod
    async def create(
        self,
        question_type: QuestionTypes,
        question_text: str,
        options: set[str],
        extra_options: set[str],
        creator_id: UUID,
    ) -> Question:
        ...


class BaseUnitOfWork(abc.ABC):  # pragma: no cover
    user_services: BaseUserServices
    question_services: BaseQuestionServices

    @abc.abstractmethod
    async def commit(self) -> None:
        ...

    @abc.abstractmethod
    async def rollback(self) -> None:
        ...

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType
    ) -> bool | None:
        await self.rollback()
        return None

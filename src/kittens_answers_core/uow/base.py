import abc
from types import TracebackType
from typing import Generic, Self, TypeVar

from kittens_answers_core.repositories.base.answer import BaseAnswerRepository
from kittens_answers_core.repositories.base.question import (
    BaseQuestionRepository,
)
from kittens_answers_core.repositories.base.user import BaseUserRepository

UT = TypeVar("UT", bound=BaseUserRepository)
QT = TypeVar("QT", bound=BaseQuestionRepository)
AT = TypeVar("AT", bound=BaseAnswerRepository)


class BaseUnitOfWork(abc.ABC, Generic[UT, QT, AT]):  # pragma: no cover
    user_services: UT
    question_services: QT
    answer_services: AT

    @property
    def services(self) -> list[UT | QT | AT]:
        return [self.user_services, self.question_services, self.answer_services]

    @abc.abstractmethod
    async def commit(self) -> None:
        ...

    async def __aenter__(self) -> Self:
        return self

    @abc.abstractmethod
    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType
    ) -> bool | None:
        ...

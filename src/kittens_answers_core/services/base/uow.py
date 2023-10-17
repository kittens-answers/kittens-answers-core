import abc
from types import TracebackType
from typing import Self

from kittens_answers_core.services.base.answer_services import BaseAnswerServices
from kittens_answers_core.services.base.question_services import BaseQuestionServices
from kittens_answers_core.services.base.user_services import BaseUserServices


class BaseUnitOfWork(abc.ABC):  # pragma: no cover
    user_services: BaseUserServices
    question_services: BaseQuestionServices

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

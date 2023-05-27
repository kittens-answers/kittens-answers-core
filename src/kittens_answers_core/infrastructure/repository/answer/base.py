import abc
from typing import Mapping

from ....domain.entities.entities import Answer, Question, User


class AnswerRepository(abc.ABC):  # pragma: no cover
    async def create_answer(
        self, user: User, question: Question, value: str | frozenset[str] | tuple[str, ...] | Mapping[str, str]
    ) -> Answer:
        ...

    async def get_answer(
        self, question: Question, value: str | frozenset[str] | tuple[str, ...] | Mapping[str, str]
    ) -> Answer:
        ...


class AnswerRepositoryException(Exception):
    ...


class AnswerAlreadyExistException(AnswerRepositoryException):
    ...


class AnswerNotFound(AnswerRepositoryException):
    ...

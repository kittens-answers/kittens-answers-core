import abc
from typing import Mapping

from ....domain.entities.entities import Answer, QuestionType, QuestionWithAnswer, User


class QuestionRepository(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    async def get_by_questions_id(self, question_id: int) -> tuple[QuestionWithAnswer[Answer]]:
        ...

    @abc.abstractmethod
    async def get_by_answer_id(self, answer_id: int) -> QuestionWithAnswer[Answer]:
        ...

    @abc.abstractmethod
    async def list(self) -> tuple[QuestionWithAnswer[Answer]]:
        ...

    @abc.abstractmethod
    async def create(
        self,
        user: User,
        question_text: str,
        question_type: QuestionType,
        options: frozenset[str],
        extra_options: frozenset[str],
        answer: str | frozenset[str] | tuple[str, ...] | Mapping[str, str],
        is_correct: bool,
    ) -> QuestionWithAnswer[Answer]:
        ...


class QuestionRepositoryException(Exception):
    ...


class QuestionNotFoundException(QuestionRepositoryException):
    ...


class QuestionAlreadyExistException(QuestionRepositoryException):
    ...


class AnswerNotFoundException(QuestionRepositoryException):
    ...

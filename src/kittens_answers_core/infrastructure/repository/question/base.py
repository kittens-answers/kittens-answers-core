import abc

from ....domain.entities.entities import Question, QuestionType, User


class QuestionRepository(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    async def get_by_id(self, question_id: int) -> Question:
        ...

    @abc.abstractmethod
    async def list(self) -> tuple[Question, ...]:
        ...

    @abc.abstractmethod
    async def create(
        self,
        user: User,
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


class QuestionRepositoryException(Exception):
    ...


class QuestionNotFoundException(QuestionRepositoryException):
    ...


class QuestionAlreadyExistException(QuestionRepositoryException):
    ...

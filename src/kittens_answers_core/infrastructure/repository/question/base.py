import abc

from ....domain.entities.entities import Question, QuestionWithoutId


class QuestionRepository(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    async def get(self, dto: QuestionWithoutId) -> Question:
        ...

    @abc.abstractmethod
    async def get_or_create(self, dto: QuestionWithoutId) -> Question:
        ...

    @abc.abstractmethod
    async def list(self) -> tuple[Question]:
        ...


class QuestionRepositoryException(Exception):
    ...


class QuestionNotFoundException(QuestionRepositoryException):
    ...


class QuestionAlreadyExistException(QuestionRepositoryException):
    ...

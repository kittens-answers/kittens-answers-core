import abc
from contextlib import AbstractAsyncContextManager

from kittens_answers_core.infrastructure.repository.abstract import (
    AbstractAnswerRepository,
    AbstractMarkRepository,
    AbstractQuestionRepository,
    AbstractUserRepository,
)


class UoW(AbstractAsyncContextManager):  # pragma: no cover
    user_repository: AbstractUserRepository
    question_repository: AbstractQuestionRepository
    answer_repository: AbstractAnswerRepository
    mark_repository: AbstractMarkRepository

    @abc.abstractmethod
    async def commit(self):
        ...

    async def rollback(self):
        ...

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.rollback()

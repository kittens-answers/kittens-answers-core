import abc
from contextlib import AbstractAsyncContextManager

from ..repository.question.base import QuestionRepository
from ..repository.user.base import UserRepository


class UoW(AbstractAsyncContextManager):  # pragma: no cover
    user_repository: UserRepository
    question_repository: QuestionRepository

    @abc.abstractmethod
    async def commit(self):
        ...

    async def rollback(self):
        ...

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.rollback()

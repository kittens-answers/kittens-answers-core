import abc
from contextlib import AbstractAsyncContextManager

from ..repository.abc_user import UserRepository


class UoW(AbstractAsyncContextManager):  # pragma: no cover
    user_repository: UserRepository

    @abc.abstractmethod
    async def commit(self):
        ...

    async def rollback(self):
        ...

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.rollback()

import abc
from types import TracebackType
from typing import Self

from kittens_answers_core.models import User


class BaseUserServices(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    async def get_by_foreign_id(self, foreign_id: str) -> User:
        ...

    @abc.abstractmethod
    async def get_by_uid(self, uid: str) -> User:
        ...

    @abc.abstractmethod
    async def create(self, foreign_id: str) -> User:
        ...


class BaseUnitOfWork(abc.ABC):  # pragma: no cover
    user_services: BaseUserServices

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

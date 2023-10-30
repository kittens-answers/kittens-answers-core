import abc
from uuid import UUID

from kittens_answers_core.models import User


class BaseUserRepository(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    async def get_by_foreign_id(self, foreign_id: str) -> User:
        ...

    @abc.abstractmethod
    async def get_by_uid(self, uid: UUID) -> User:
        ...

    @abc.abstractmethod
    async def create(self, foreign_id: str) -> User:
        ...

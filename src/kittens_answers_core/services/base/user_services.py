import abc
from typing import Any
from uuid import UUID

from kittens_answers_core.models import User


class BaseUserServices(abc.ABC):  # pragma: no cover
    def inject_service(self, obj: Any) -> None:
        obj.user_services = self

    @abc.abstractmethod
    async def get_by_foreign_id(self, foreign_id: str) -> User:
        ...

    @abc.abstractmethod
    async def get_by_uid(self, uid: UUID) -> User:
        ...

    @abc.abstractmethod
    async def create(self, foreign_id: str) -> User:
        ...

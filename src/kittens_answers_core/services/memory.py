from typing import Self, cast
from uuid import UUID, uuid4

from kittens_answers_core.models import User
from kittens_answers_core.services.base import (
    BaseUnitOfWork,
    BaseUserServices,
)
from kittens_answers_core.services.errors import UserAlreadyExistError, UserDoesNotExistError


class MemoryUserServices(BaseUserServices):
    def __init__(self) -> None:
        self.data: list[User] = []

    async def get_by_foreign_id(self, foreign_id: str) -> User:
        for user in self.data:
            if user.foreign_id == foreign_id:
                return user
        raise UserDoesNotExistError

    async def get_by_uid(self, uid: str) -> User:
        uid_ = UUID(uid)
        for user in self.data:
            if user.uid == uid_:
                return user
        raise UserDoesNotExistError

    async def create(self, foreign_id: str) -> User:
        for user in self.data:
            if user.foreign_id == foreign_id:
                raise UserAlreadyExistError
        user = User(uid=uuid4(), foreign_id=foreign_id)
        self.data.append(user)
        return user


class MemoryUnitOfWork(BaseUnitOfWork):
    def __init__(self) -> None:
        self.user_services = MemoryUserServices()
        self._user_back_up: list[str] = []

    async def commit(self) -> None:
        user_services = cast(MemoryUserServices, self.user_services)
        self._user_back_up = [user.model_dump_json() for user in user_services.data]

    async def rollback(self) -> None:
        user_services = cast(MemoryUserServices, self.user_services)
        user_services.data = [User.model_validate_json(data) for data in self._user_back_up]

    async def __aenter__(self) -> Self:
        user_services = cast(MemoryUserServices, self.user_services)
        self._user_back_up = [user.model_dump_json() for user in user_services.data]
        return await super().__aenter__()

from uuid import UUID, uuid4

from kittens_answers_core.models import User
from kittens_answers_core.services.base.repositories.user import BaseUserRepository
from kittens_answers_core.services.errors import (
    UserAlreadyExistError,
    UserDoesNotExistError,
)
from kittens_answers_core.services.memory.repositories.backup_mixin import MemoryBackUpMixin


class MemoryUserServices(BaseUserRepository, MemoryBackUpMixin[User]):
    def __init__(self, data: list[User]) -> None:
        super().__init__(User, "user", data)

    async def get_by_foreign_id(self, foreign_id: str) -> User:
        for user in self.data:
            if user.foreign_id == foreign_id:
                return user
        raise UserDoesNotExistError

    async def get_by_uid(self, uid: UUID) -> User:
        for user in self.data:
            if user.uid == uid:
                return user
        raise UserDoesNotExistError

    async def create(self, foreign_id: str) -> User:
        for user in self.data:
            if user.foreign_id == foreign_id:
                raise UserAlreadyExistError
        user = User(uid=uuid4(), foreign_id=foreign_id)
        self.data.append(user)
        return user

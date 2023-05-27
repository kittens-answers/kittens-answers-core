from ....domain.entities.entities import User
from .base import UserAlreadyExistException, UserNotFoundException, UserRepository


class MemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self._data: set[User] = set()

    def new_id(self):
        if self._data:
            return max([user.id for user in self._data]) + 1
        else:
            return 1

    async def get_by_id(self, user_id: int) -> User:
        for user in self._data:
            if user.id == user_id:
                return user
        raise UserNotFoundException

    async def get_by_public_id(self, public_id: str) -> User:
        for user in self._data:
            if user.public_id == public_id:
                return user
        raise UserNotFoundException

    async def create(self, public_id: str) -> User:
        try:
            user = await self.get_by_public_id(public_id=public_id)
        except UserNotFoundException:
            user = User(id=self.new_id(), public_id=public_id)
            self._data.add(user)
            return user
        raise UserAlreadyExistException

    async def list(self) -> tuple[User, ...]:
        return tuple(self._data)

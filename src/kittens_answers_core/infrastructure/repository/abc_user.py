import abc

from ...domain.entities.entities import User


class UserRepository(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    async def create(self, public_id: str) -> User:
        ...

    @abc.abstractmethod
    async def get_by_public_id(self, public_id: str) -> User:
        ...

    @abc.abstractmethod
    async def get_by_id(self, user_id: int) -> User:
        ...

    @abc.abstractmethod
    async def list(self) -> tuple[User, ...]:
        ...


class UserRepositoryException(Exception):
    ...


class UserNotFoundException(UserRepositoryException):
    ...


class UserAlreadyExistException(UserRepositoryException):
    ...

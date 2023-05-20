import pytest

from kittens_answers_core.infrastructure.repository.user.base import (
    UserAlreadyExistException,
    UserNotFoundException,
    UserRepository,
)
from kittens_answers_core.infrastructure.repository.user.memory import (
    MemoryUserRepository,
)

pytestmark = pytest.mark.anyio


@pytest.fixture
def user_repo():
    return MemoryUserRepository()


async def test_get_by_id(user_repo: UserRepository):
    with pytest.raises(UserNotFoundException):
        await user_repo.get_by_id(user_id=1)

    user_1 = await user_repo.create("user")

    user_2 = await user_repo.get_by_id(user_1.id)

    assert user_1 == user_2


async def test_get_by_public_id(user_repo: UserRepository):
    with pytest.raises(UserNotFoundException):
        await user_repo.get_by_public_id("user")

    user_1 = await user_repo.create("user")

    user_2 = await user_repo.get_by_public_id("user")

    assert user_1 == user_2


async def test_create(user_repo: UserRepository):
    user_1 = await user_repo.create("user")

    with pytest.raises(UserAlreadyExistException):
        await user_repo.create("user")

    user_2 = await user_repo.create("new user")

    assert user_1 != user_2

    assert user_1.id != user_2.id


async def test_list(user_repo: UserRepository):
    assert len(await user_repo.list()) == 0

    user_1 = await user_repo.create("user_1")

    assert user_1 in (await user_repo.list())

    user_2 = await user_repo.create("user_2")

    assert user_1 in (await user_repo.list())
    assert user_2 in (await user_repo.list())

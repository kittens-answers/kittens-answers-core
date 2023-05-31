import pytest

from kittens_answers_core.domain.entities import User
from kittens_answers_core.infrastructure.repository.exception import (
    UserAlreadyExistException,
    UserNotFoundException,
)
from kittens_answers_core.infrastructure.unit_of_work.abc_uow import UoW

pytestmark = pytest.mark.anyio


async def test_get_by_id_if_not_exist(uow: UoW):
    async with uow:
        with pytest.raises(UserNotFoundException):
            await uow.user_repository.get_by_id(user_id=1)
            await uow.commit()


async def test_get_by_id_if_exist(uow: UoW, user: User):
    async with uow:
        user_2 = await uow.user_repository.get_by_id(user.id)
        await uow.commit()

    assert user == user_2


async def test_get_by_public_id_if_not_exist(uow: UoW):
    async with uow:
        with pytest.raises(UserNotFoundException):
            await uow.user_repository.get_by_public_id("user")
            await uow.commit()


async def test_get_by_public_id_if_exist(uow: UoW, user: User):
    async with uow:
        user_2 = await uow.user_repository.get_by_public_id(user.public_id)
        await uow.commit()

    assert user == user_2


async def test_create_if_not_exist(uow: UoW):
    async with uow:
        await uow.user_repository.create("user")
        await uow.commit()


async def test_create_if_exist(uow: UoW, user: User):
    async with uow:
        with pytest.raises(UserAlreadyExistException):
            await uow.user_repository.create(user.public_id)
            await uow.commit()

    async with uow:
        user_2 = await uow.user_repository.create("new user")
        await uow.commit()

    assert user != user_2

    assert user.id != user_2.id


async def test_list(uow: UoW):
    async with uow:
        assert len(await uow.user_repository.list()) == 0

    async with uow:
        user_1 = await uow.user_repository.create("user_1")
        await uow.commit()

    async with uow:
        assert user_1 in (await uow.user_repository.list())

    async with uow:
        user_2 = await uow.user_repository.create("user_2")
        await uow.commit()

    async with uow:
        assert user_1 in (await uow.user_repository.list())
        assert user_2 in (await uow.user_repository.list())

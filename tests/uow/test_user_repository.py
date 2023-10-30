import pytest

from kittens_answers_core.services.errors import (
    UserAlreadyExistError,
    UserDoesNotExistError,
)
from tests.uow.fixture_types import UIDFactory, UOWTypes, UserDataFactory, UserFactory

pytestmark = pytest.mark.anyio


class TestGetByForeignID:
    async def test_if_not_in_db(self, uow: UOWTypes, user_data_factory: UserDataFactory) -> None:
        with pytest.raises(UserDoesNotExistError):
            async with uow:
                await uow.user_services.get_by_foreign_id(**user_data_factory())

    async def test_if_in_db(self, uow: UOWTypes, user_factory: UserFactory) -> None:
        user_in_db = await user_factory()
        async with uow:
            user = await uow.user_services.get_by_foreign_id(foreign_id=user_in_db.foreign_id)
            await uow.commit()

        assert user == user_in_db


class TestGetByUid:
    async def test_if_not_in_db(self, uow: UOWTypes, uid_factory: UIDFactory) -> None:
        with pytest.raises(UserDoesNotExistError):
            async with uow:
                await uow.user_services.get_by_uid(uid=uid_factory())

    async def test_if_in_db(self, uow: UOWTypes, user_factory: UserFactory) -> None:
        user_in_db = await user_factory()
        async with uow:
            user = await uow.user_services.get_by_uid(uid=user_in_db.uid)
            await uow.commit()

        assert user == user_in_db


class TestCreate:
    async def test_if_not_in_db(self, uow: UOWTypes, user_data_factory: UserDataFactory) -> None:
        async with uow:
            user = await uow.user_services.create(**user_data_factory())
            await uow.commit()

        assert user

    async def test_if_in_db(self, uow: UOWTypes, user_factory: UserFactory) -> None:
        user_in_db = await user_factory()
        with pytest.raises(UserAlreadyExistError):
            async with uow:
                await uow.user_services.create(foreign_id=user_in_db.foreign_id)

    async def test_rollback(self, uow: UOWTypes, user_data_factory: UserDataFactory) -> None:
        user_data = user_data_factory()
        async with uow:
            await uow.user_services.create(**user_data)

        with pytest.raises(UserDoesNotExistError):
            async with uow:
                await uow.user_services.get_by_foreign_id(foreign_id=user_data["foreign_id"])

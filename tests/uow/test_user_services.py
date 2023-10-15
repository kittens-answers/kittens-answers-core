from collections.abc import Callable
from uuid import UUID

import pytest

from kittens_answers_core.models import User
from kittens_answers_core.services.base import BaseUnitOfWork
from kittens_answers_core.services.errors import UserAlreadyExistError, UserDoesNotExistError

pytestmark = pytest.mark.anyio


class TestGetByForeignID:
    @pytest.mark.usefixtures("populate_users")
    async def test_if_not_in_db(self, uow: BaseUnitOfWork, user_foreign_id_factory: Callable[..., str]) -> None:
        with pytest.raises(UserDoesNotExistError):
            async with uow:
                await uow.user_services.get_by_foreign_id(foreign_id=user_foreign_id_factory())

    async def test_if_in_db(self, uow: BaseUnitOfWork, populate_users: list[User]) -> None:
        user_in_db = populate_users[0]
        async with uow:
            user = await uow.user_services.get_by_foreign_id(foreign_id=user_in_db.foreign_id)
            await uow.commit()

        assert user == user_in_db


class TestGetByUid:
    async def test_if_not_in_db(
        self, uow: BaseUnitOfWork, populate_users: list[User], user_uid_factory: Callable[..., UUID]
    ) -> None:
        while True:
            user_uid = user_uid_factory()
            if user_uid not in [user.uid for user in populate_users]:
                break
        with pytest.raises(UserDoesNotExistError):
            async with uow:
                await uow.user_services.get_by_uid(uid=user_uid)

    async def test_if_in_db(self, uow: BaseUnitOfWork, populate_users: list[User]) -> None:
        user_in_db = populate_users[0]
        async with uow:
            user = await uow.user_services.get_by_uid(uid=user_in_db.uid)
            await uow.commit()

        assert user == user_in_db


class TestCreate:
    @pytest.mark.usefixtures("populate_users")
    async def test_if_not_in_db(self, uow: BaseUnitOfWork, user_foreign_id_factory: Callable[..., str]) -> None:
        async with uow:
            user = await uow.user_services.create(foreign_id=user_foreign_id_factory())
            await uow.commit()

        assert user

    async def test_if_in_db(self, uow: BaseUnitOfWork, populate_users: list[User]) -> None:
        user_in_db = populate_users[0]
        with pytest.raises(UserAlreadyExistError):
            async with uow:
                await uow.user_services.create(foreign_id=user_in_db.foreign_id)

    @pytest.mark.usefixtures("populate_users")
    async def test_rollback(self, uow: BaseUnitOfWork, user_foreign_id_factory: Callable[..., str]) -> None:
        foreign_id = user_foreign_id_factory()
        async with uow:
            await uow.user_services.create(foreign_id=foreign_id)
            await uow.rollback()

        with pytest.raises(UserDoesNotExistError):
            async with uow:
                await uow.user_services.get_by_foreign_id(foreign_id=foreign_id)

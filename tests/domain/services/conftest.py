import pytest

from kittens_answers_core.domain.services.user import get_or_create
from kittens_answers_core.infrastructure.unit_of_work.abc_uow import UoW


@pytest.fixture
async def user(uow: UoW):
    async with uow:
        user = await get_or_create("user", uow=uow)
        await uow.commit()
    return user

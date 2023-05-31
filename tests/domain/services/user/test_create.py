import pytest

from kittens_answers_core.domain.services.user import get_or_create
from kittens_answers_core.infrastructure.unit_of_work.abc_uow import UoW

pytestmark = pytest.mark.anyio


async def test_get_or_create(uow: UoW):
    await get_or_create("user", uow=uow)

    assert len(await uow.user_repository.list()) == 1

    await get_or_create("user", uow=uow)

    assert len(await uow.user_repository.list()) == 1

    await get_or_create("other", uow=uow)

    assert len(await uow.user_repository.list()) == 2

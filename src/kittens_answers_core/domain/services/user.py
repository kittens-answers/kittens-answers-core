from kittens_answers_core.infrastructure.repository.exception import (
    UserNotFoundException,
)
from kittens_answers_core.infrastructure.unit_of_work.abc_uow import UoW


async def get_or_create(user_public_id: str, uow: UoW):
    async with uow:
        try:
            user = await uow.user_repository.get_by_public_id(public_id=user_public_id)
        except UserNotFoundException:
            user = await uow.user_repository.create(public_id=user_public_id)
            await uow.commit()
    return user

from ...infrastructure.repository.user.base import UserNotFoundException
from ...infrastructure.unit_of_work.abc_uow import UoW


async def get_or_create(user_public_id: str, uow: UoW):
    try:
        user = await uow.user_repository.get_by_public_id(public_id=user_public_id)
    except UserNotFoundException:
        user = await uow.user_repository.create(public_id=user_public_id)
    return user

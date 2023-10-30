from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from kittens_answers_core.models import User
from kittens_answers_core.services.base.repositories.user import BaseUserRepository
from kittens_answers_core.services.db.models import DBUser
from kittens_answers_core.services.errors import (
    UserAlreadyExistError,
    UserDoesNotExistError,
)


class SQLAlchemyUserRepository(BaseUserRepository):
    session: AsyncSession

    async def get_by_foreign_id(self, foreign_id: str) -> User:
        user = await self.session.scalar(select(DBUser).where(DBUser.foreign_id == foreign_id))
        if user is None:
            raise UserDoesNotExistError
        return User(uid=user.uid, foreign_id=user.foreign_id)

    async def get_by_uid(self, uid: UUID) -> User:
        user = await self.session.scalar(select(DBUser).where(DBUser.uid == uid))
        if user is None:
            raise UserDoesNotExistError
        return User(uid=user.uid, foreign_id=user.foreign_id)

    async def create(self, foreign_id: str) -> User:
        user = DBUser(foreign_id=foreign_id, uid=uuid4())
        self.session.add(user)
        try:
            await self.session.flush()
        except IntegrityError as error:
            raise UserAlreadyExistError from error
        return User(uid=user.uid, foreign_id=user.foreign_id)

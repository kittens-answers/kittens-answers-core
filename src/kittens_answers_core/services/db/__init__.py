from types import TracebackType
from typing import Self
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from kittens_answers_core.models import User
from kittens_answers_core.services.base import BaseUnitOfWork, BaseUserServices
from kittens_answers_core.services.db.models import User as DBUser
from kittens_answers_core.services.errors import UserAlreadyExistError, UserDoesNotExistError


class SQLAlchemyUnitOfWork(BaseUnitOfWork):
    session: AsyncSession

    def __init__(self, db_url: str) -> None:
        self._engine = create_async_engine(url=db_url)
        self.session_factory = async_sessionmaker(bind=self._engine, expire_on_commit=False)

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def __aenter__(self) -> Self:
        self.session = AsyncSession(bind=self._engine)
        self.user_services = SQLAlchemyUserServices(session=self.session)
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType
    ) -> bool | None:
        await super().__aexit__(exc_type, exc_value, traceback)
        await self.session.close()
        delattr(self, "user_services")
        return None


class SQLAlchemyUserServices(BaseUserServices):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_foreign_id(self, foreign_id: str) -> User:
        user = await self.session.scalar(select(DBUser).where(DBUser.foreign_id == foreign_id))
        if user is None:
            raise UserDoesNotExistError
        return User(uid=user.uid, foreign_id=user.foreign_id)

    async def get_by_uid(self, uid: str) -> User:
        user = await self.session.scalar(select(DBUser).where(DBUser.uid == UUID(uid)))
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

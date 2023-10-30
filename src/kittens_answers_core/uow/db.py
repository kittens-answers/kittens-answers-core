from types import TracebackType
from typing import Self, TypeAlias

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from kittens_answers_core.repositories.db.answer import (
    SQLAlchemyAnswerRepository,
)
from kittens_answers_core.repositories.db.question import (
    SQLAlchemyQuestionRepository,
)
from kittens_answers_core.repositories.db.user import SQLAlchemyUserRepository
from kittens_answers_core.uow.base import BaseUnitOfWork

SQLAlchemyServices: TypeAlias = SQLAlchemyUserRepository | SQLAlchemyQuestionRepository


class SQLAlchemyUnitOfWork(
    BaseUnitOfWork[SQLAlchemyUserRepository, SQLAlchemyQuestionRepository, SQLAlchemyAnswerRepository]
):
    session: AsyncSession

    def __init__(self, db_url: str) -> None:
        self._engine = create_async_engine(url=db_url)
        self.session_factory = async_sessionmaker(bind=self._engine, expire_on_commit=False)
        self.user_services = SQLAlchemyUserRepository()
        self.question_services = SQLAlchemyQuestionRepository()
        self.answer_services = SQLAlchemyAnswerRepository()

    async def commit(self) -> None:
        await self.session.commit()

    async def __aenter__(self) -> Self:
        self.session = AsyncSession(bind=self._engine)
        for service in self.services:
            service.session = self.session
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType
    ) -> bool | None:
        await self.session.rollback()
        await self.session.close()
        for service in self.services:
            delattr(service, "session")
        return None

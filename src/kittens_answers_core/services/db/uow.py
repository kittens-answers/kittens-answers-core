from types import TracebackType
from typing import Self, TypeAlias

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from kittens_answers_core.services.base.uow import BaseUnitOfWork
from kittens_answers_core.services.db.question_services import SQLAlchemyQuestionServices
from kittens_answers_core.services.db.session_mixin import SessionMixin
from kittens_answers_core.services.db.user_services import SQLAlchemyUserServices

SQLAlchemyServices: TypeAlias = SQLAlchemyUserServices | SQLAlchemyQuestionServices


class SQLAlchemyUnitOfWork(BaseUnitOfWork, SessionMixin):
    session: AsyncSession
    _services_types: tuple[type[SQLAlchemyServices], ...] = (
        SQLAlchemyUserServices,
        SQLAlchemyQuestionServices,
    )

    def __init__(self, db_url: str) -> None:
        self._services: list[SQLAlchemyServices] = []
        self._engine = create_async_engine(url=db_url)
        self.session_factory = async_sessionmaker(bind=self._engine, expire_on_commit=False)
        for service_type in self._services_types:
            service = service_type()
            self._services.append(service)
            service.inject_service(self)

    async def commit(self) -> None:
        await self.session.commit()

    async def __aenter__(self) -> Self:
        self.session = AsyncSession(bind=self._engine)
        for service in self._services:
            service.session = self.session
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType
    ) -> bool | None:
        await self.session.rollback()
        await self.session.close()
        for service in self._services:
            service.delete_session()
        return None

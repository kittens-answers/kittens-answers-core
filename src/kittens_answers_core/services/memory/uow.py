from types import TracebackType
from typing import Self, TypeAlias

from kittens_answers_core.services.base.uow import BaseUnitOfWork
from kittens_answers_core.services.memory.question_services import MemoryQuestionServices
from kittens_answers_core.services.memory.user_services import MemoryUserServices

MemoryServices: TypeAlias = MemoryUserServices | MemoryQuestionServices


class MemoryUnitOfWork(BaseUnitOfWork):
    _services_types: tuple[type[MemoryServices], ...] = (
        MemoryUserServices,
        MemoryQuestionServices,
    )

    def __init__(self) -> None:
        self._services: list[MemoryServices] = []
        for service_type in self._services_types:
            service = service_type([])
            self._services.append(service)
            service.inject_service(self)

    async def commit(self) -> None:
        for service in self._services:
            service.make_backup()

    async def __aenter__(self) -> Self:
        for service in self._services:
            service.make_backup()
        return await super().__aenter__()

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType
    ) -> bool | None:
        for service in self._services:
            service.rollback_backup()
        return None

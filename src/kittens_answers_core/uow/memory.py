from types import TracebackType
from typing import Self, TypeAlias

from kittens_answers_core.repositories.memory.answer import MemoryAnswerServices
from kittens_answers_core.repositories.memory.question import MemoryQuestionServices
from kittens_answers_core.repositories.memory.user import MemoryUserServices
from kittens_answers_core.uow.base import BaseUnitOfWork

MemoryServices: TypeAlias = MemoryUserServices | MemoryQuestionServices | MemoryAnswerServices


class MemoryUnitOfWork(BaseUnitOfWork[MemoryUserServices, MemoryQuestionServices, MemoryAnswerServices]):
    def __init__(self) -> None:
        self.user_services = MemoryUserServices([])
        self.question_services = MemoryQuestionServices([])
        self.answer_services = MemoryAnswerServices([])

    async def commit(self) -> None:
        for service in self.services:
            service.make_backup()

    async def __aenter__(self) -> Self:
        for service in self.services:
            service.make_backup()
        return await super().__aenter__()

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType
    ) -> bool | None:
        for service in self.services:
            service.rollback_backup()
        return None

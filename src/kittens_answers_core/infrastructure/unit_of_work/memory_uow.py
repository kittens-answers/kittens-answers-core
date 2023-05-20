from copy import deepcopy
from typing import cast

from ..repository.question.memory import MemoryQuestionRepository
from ..repository.user.memory import MemoryUserRepository
from .abc_uow import UoW


class MemoryUoW(UoW):
    def __init__(self) -> None:
        self.user_repository = MemoryUserRepository()
        self.question_repository = MemoryQuestionRepository()

    async def __aenter__(self):
        self._old_user_data = deepcopy(cast(MemoryUserRepository, self.user_repository)._data)
        self._old_question_data = deepcopy(cast(MemoryQuestionRepository, self.question_repository)._data)
        return self

    async def rollback(self):
        if hasattr(self, "_old_user_data"):
            cast(MemoryUserRepository, self.user_repository)._data = self._old_user_data
        if hasattr(self, "_old_question_data"):
            cast(MemoryQuestionRepository, self.question_repository)._data = self._old_question_data

    async def commit(self):
        del self._old_user_data
        del self._old_question_data

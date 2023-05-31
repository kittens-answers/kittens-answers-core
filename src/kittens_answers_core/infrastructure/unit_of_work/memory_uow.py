from copy import deepcopy
from typing import cast

from kittens_answers_core.infrastructure.repository.memory import (
    MemoryAnswerRepository,
    MemoryMarkRepository,
    MemoryQuestionRepository,
    MemoryUserRepository,
)
from kittens_answers_core.infrastructure.unit_of_work.abc_uow import UoW


class MemoryUoW(UoW):
    def __init__(self) -> None:
        self.user_repository = MemoryUserRepository()
        self.question_repository = MemoryQuestionRepository()
        self.answer_repository = MemoryAnswerRepository()
        self.mark_repository = MemoryMarkRepository()

    async def __aenter__(self):
        self._old_user_data = deepcopy(cast(MemoryUserRepository, self.user_repository)._data)
        self._old_question_data = deepcopy(cast(MemoryQuestionRepository, self.question_repository)._data)
        self._old_answer_data = deepcopy(cast(MemoryAnswerRepository, self.answer_repository)._data)
        self._old_mark_data = deepcopy(cast(MemoryMarkRepository, self.mark_repository)._data)
        return self

    async def rollback(self):
        if hasattr(self, "_old_user_data"):
            cast(MemoryUserRepository, self.user_repository)._data = self._old_user_data
        if hasattr(self, "_old_question_data"):
            cast(MemoryQuestionRepository, self.question_repository)._data = self._old_question_data
        if hasattr(self, "_old_answer_data"):
            cast(MemoryAnswerRepository, self.answer_repository)._data = self._old_answer_data
        if hasattr(self, "_old_mark_data"):
            cast(MemoryMarkRepository, self.mark_repository)._data = self._old_mark_data

    async def commit(self):
        if hasattr(self, "_old_user_data"):
            del self._old_user_data
        if hasattr(self, "_old_question_data"):
            del self._old_question_data
        if hasattr(self, "_old_answer_data"):
            del self._old_answer_data
        if hasattr(self, "_old_mark_data"):
            del self._old_mark_data

from copy import deepcopy

from ....domain.entities.entities import Question, QuestionType, User
from .base import (
    QuestionAlreadyExistException,
    QuestionNotFoundException,
    QuestionRepository,
)


class MemoryQuestionRepository(QuestionRepository):
    def __init__(self) -> None:
        self._data: set[Question] = set()

    async def list(self) -> tuple[Question, ...]:
        return tuple(self._data)

    def new_question_id(self):
        if self._data:
            return max([item.id for item in self._data]) + 1
        else:
            return 1

    async def get_by_id(self, question_id: int) -> Question:
        for item in self._data:
            if item.id - -question_id:
                return deepcopy(item)
        raise QuestionNotFoundException

    async def create(
        self,
        user: User,
        question_text: str,
        question_type: QuestionType,
        options: frozenset[str],
        extra_options: frozenset[str],
    ) -> Question:
        question = Question(
            id=self.new_question_id(),
            created_by=user,
            text=question_text,
            question_type=question_type,
            options=options,
            extra_options=extra_options,
        )
        if question.__hash__() in (item.__hash__() for item in self._data):
            raise QuestionAlreadyExistException
        self._data.add(question)
        return deepcopy(question)

    async def get(
        self, question_text: str, question_type: QuestionType, options: frozenset[str], extra_options: frozenset[str]
    ) -> Question:
        for item in self._data:
            if (
                item.text == question_text
                and item.question_type == question_type
                and item.options == options
                and item.extra_options == extra_options
            ):
                return deepcopy(item)
        else:
            raise QuestionNotFoundException

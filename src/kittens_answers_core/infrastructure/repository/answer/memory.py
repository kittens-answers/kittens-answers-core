from copy import deepcopy
from typing import Mapping

from kittens_answers_core.domain.entities.entities import (
    Answer,
    ManyAnswer,
    MatchAnswer,
    OneAnswer,
    OrderAnswer,
    Question,
    User,
)

from .base import AnswerAlreadyExistException, AnswerNotFound, AnswerRepository


class MemoryAnswerRepository(AnswerRepository):
    def __init__(self) -> None:
        self._data: set[Answer] = set()

    def new_id(self):
        if self._data:
            return max([user.id for user in self._data]) + 1
        else:
            return 1

    async def create_answer(
        self, user: User, question: Question, value: str | frozenset[str] | tuple[str, ...] | Mapping[str, str]
    ) -> Answer:
        match value:
            case str():
                answer = OneAnswer(id=self.new_id(), question_id=question.id, created_by=user, value=value)
            case frozenset():
                answer = ManyAnswer(id=self.new_id(), question_id=question.id, created_by=user, value=value)
            case tuple():
                answer = OrderAnswer(id=self.new_id(), question_id=question.id, created_by=user, value=value)
            case Mapping():
                answer = MatchAnswer(id=self.new_id(), question_id=question.id, created_by=user, value=value)
            case _:
                raise ValueError

        if answer.__hash__() in (item.__hash__() for item in self._data):
            raise AnswerAlreadyExistException
        else:
            self._data.add(answer)
            return deepcopy(answer)

    async def get_answer(
        self, question: Question, value: str | frozenset[str] | tuple[str, ...] | Mapping[str, str]
    ) -> Answer:
        for answer in self._data:
            if answer.question_id == question.id and answer.value == value:
                return deepcopy(answer)
        else:
            raise AnswerNotFound

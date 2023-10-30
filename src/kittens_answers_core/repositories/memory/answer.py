from uuid import UUID

from kittens_answers_core.errors import (
    AnswerAlreadyExistError,
    AnswerDoesNotExistError,
)
from kittens_answers_core.models import Answer
from kittens_answers_core.repositories.base.answer import BaseAnswerRepository
from kittens_answers_core.repositories.memory.backup_mixin import MemoryBackUpMixin


class MemoryAnswerServices(BaseAnswerRepository, MemoryBackUpMixin[Answer]):
    def __init__(self, data: list[Answer]) -> None:
        super().__init__(Answer, "answer", data)

    async def create(
        self, answer: list[str], extra_answer: list[str], question_uid: UUID, creator_id: UUID, *, is_correct: bool
    ) -> Answer:
        for _answer in self.data:
            if (
                _answer.answer == answer
                and _answer.extra_answer == extra_answer
                and _answer.question_uid == question_uid
                and _answer.is_correct == is_correct
            ):
                raise AnswerAlreadyExistError
        _answer = Answer(
            creator=creator_id,
            question_uid=question_uid,
            answer=answer,
            extra_answer=extra_answer,
            is_correct=is_correct,
        )
        self.data.append(_answer)
        return _answer

    async def get(self, answer: list[str], extra_answer: list[str], question_uid: UUID, *, is_correct: bool) -> Answer:
        for _answer in self.data:
            if (
                _answer.answer == answer
                and _answer.extra_answer == extra_answer
                and _answer.question_uid == question_uid
                and _answer.is_correct == is_correct
            ):
                return _answer
        raise AnswerDoesNotExistError

    async def get_by_uid(self, answer_uid: UUID) -> Answer:
        for _answer in self.data:
            if _answer.uid == answer_uid:
                return _answer
        raise AnswerDoesNotExistError

import abc
from typing import Any
from uuid import UUID

from kittens_answers_core.models import Answer


class BaseAnswerRepository(abc.ABC):  # pragma: no cover
    def __set_name__(self, owner: Any, name: str) -> None:
        self.name = name

    @abc.abstractmethod
    async def create(
        self,
        answer: list[str],
        extra_answer: list[str],
        question_uid: UUID,
        creator_id: UUID,
        *,
        is_correct: bool,
    ) -> Answer:
        ...

    @abc.abstractmethod
    async def get(
        self,
        answer: list[str],
        extra_answer: list[str],
        question_uid: UUID,
        *,
        is_correct: bool,
    ) -> Answer:
        ...

    @abc.abstractmethod
    async def get_by_uid(self, answer_uid: UUID) -> Answer:
        ...

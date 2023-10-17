import abc
from typing import Any
from uuid import UUID

from kittens_answers_core.models import Question, QuestionTypes


class BaseQuestionServices(abc.ABC):  # pragma: no cover
    def inject_service(self, obj: Any) -> None:
        obj.question_services = self

    @abc.abstractmethod
    async def get_by_uid(self, uid: UUID) -> Question:
        ...

    @abc.abstractmethod
    async def get(
        self,
        question_type: QuestionTypes,
        question_text: str,
        options: set[str],
        extra_options: set[str],
    ) -> Question:
        ...

    @abc.abstractmethod
    async def create(
        self,
        question_type: QuestionTypes,
        question_text: str,
        options: set[str],
        extra_options: set[str],
        creator_id: UUID,
    ) -> Question:
        ...

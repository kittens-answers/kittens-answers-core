from uuid import UUID

from kittens_answers_core.errors import (
    QuestionAlreadyExistError,
    QuestionDoesNotExistError,
)
from kittens_answers_core.models import Question, QuestionTypes
from kittens_answers_core.repositories.base.question import (
    BaseQuestionRepository,
)
from kittens_answers_core.repositories.memory.backup_mixin import MemoryBackUpMixin


class MemoryQuestionServices(BaseQuestionRepository, MemoryBackUpMixin[Question]):
    def __init__(self, data: list[Question]) -> None:
        super().__init__(Question, "question", data)

    async def create(
        self,
        question_type: QuestionTypes,
        question_text: str,
        options: set[str],
        extra_options: set[str],
        creator_id: UUID,
    ) -> Question:
        for question in self.data:
            if (
                question.question_type == question_type
                and question.text == question_text
                and question.options == options
                and question.extra_options == extra_options
            ):
                raise QuestionAlreadyExistError
        question = Question(
            creator=creator_id,
            question_type=question_type,
            text=question_text,
            options=options,
            extra_options=extra_options,
        )
        self.data.append(question)
        return question

    async def get_by_uid(self, uid: UUID) -> Question:
        for question in self.data:
            if question.uid == uid:
                return question
        raise QuestionDoesNotExistError

    async def get(
        self, question_type: QuestionTypes, question_text: str, options: set[str], extra_options: set[str]
    ) -> Question:
        for question in self.data:
            if (
                question.question_type == question_type
                and question.text == question_text
                and question.options == options
                and question.extra_options == extra_options
            ):
                return question
        raise QuestionDoesNotExistError

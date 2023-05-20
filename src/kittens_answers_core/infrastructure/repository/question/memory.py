from ....domain.entities.entities import Question, QuestionWithoutId
from .base import QuestionNotFoundException, QuestionRepository


class MemoryQuestionRepository(QuestionRepository):
    def __init__(self) -> None:
        self._data: set[Question] = set()

    def new_id(self):
        if self._data:
            return max([question.id for question in self._data]) + 1
        else:
            return 1

    async def get(self, dto: QuestionWithoutId) -> Question:
        for question in self._data:
            if (
                dto.text == question.text
                and dto.question_type == question.question_type
                and dto.options == question.options
            ):
                return question
        raise QuestionNotFoundException

    async def get_or_create(self, dto: QuestionWithoutId) -> Question:
        try:
            question = await self.get(dto=dto)
            return question
        except QuestionNotFoundException:
            question = Question(
                created_by=dto.created_by,
                text=dto.text,
                question_type=dto.question_type,
                options=dto.options,
                id=self.new_id(),
            )
            self._data.add(question)
            return question

    async def list(self) -> tuple[Question]:
        return tuple(self._data)

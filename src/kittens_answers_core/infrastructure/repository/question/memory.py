from copy import deepcopy
from typing import Mapping

from ....domain.entities.entities import (
    Answer,
    ManyAnswer,
    Mark,
    MatchAnswer,
    OneAnswer,
    Options,
    OrderAnswer,
    Question,
    QuestionType,
    QuestionWithAnswer,
    User,
)
from .base import AnswerNotFoundException, QuestionRepository


class MemoryQuestionRepository(QuestionRepository):
    def __init__(self) -> None:
        self._data: set[QuestionWithAnswer[Answer]] = set()

    async def list(self) -> tuple[QuestionWithAnswer[Answer]]:
        return tuple(self._data)

    def new_question_id(self):
        if self._data:
            return max([item.question.id for item in self._data]) + 1
        else:
            return 1

    def new_answer_id(self):
        if self._data:
            return max([item.answer.id for item in self._data]) + 1
        else:
            return 1

    async def get_by_questions_id(self, question_id: int) -> tuple[QuestionWithAnswer[Answer]]:
        return tuple(deepcopy(item) for item in self._data if item.question.id == question_id)

    async def get_by_answer_id(self, answer_id: int) -> QuestionWithAnswer[Answer]:
        for item in self._data:
            if item.answer.id == answer_id:
                return deepcopy(item)
        raise AnswerNotFoundException

    async def create(
        self,
        user: User,
        question_text: str,
        question_type: QuestionType,
        options: frozenset[str],
        extra_options: frozenset[str],
        answer: str | frozenset[str] | tuple[str, ...] | Mapping[str, str],
        is_correct: bool,
    ) -> QuestionWithAnswer:
        def is_equal(item: QuestionWithAnswer[Answer]) -> bool:
            return all(
                (
                    question_text == item.question.text,
                    question_type == item.question.question_type,
                    item.question.options == Options(options=options, extra_options=extra_options),
                    answer == item.answer.value,
                )
            )

        for item in self._data:
            if is_equal(item):
                mark = Mark(user=user, is_correct=is_correct)
                item.answer.marks.add(mark)
                return deepcopy(item)
        else:
            question = Question(
                id=self.new_question_id(),
                created_by=user,
                text=question_text,
                question_type=question_type,
                options=Options(options=options, extra_options=extra_options),
            )
            match answer:
                case str():
                    _answer = OneAnswer(
                        marks=set((Mark(user=user, is_correct=is_correct),)),
                        id=self.new_answer_id(),
                        value=answer,
                    )
                case tuple():
                    _answer = OrderAnswer(
                        marks=set((Mark(user=user, is_correct=is_correct),)),
                        id=self.new_answer_id(),
                        value=answer,
                    )
                case frozenset():
                    _answer = ManyAnswer(
                        marks=set((Mark(user=user, is_correct=is_correct),)),
                        id=self.new_answer_id(),
                        value=answer,
                    )
                case Mapping():
                    _answer = MatchAnswer(
                        marks=set((Mark(user=user, is_correct=is_correct),)),
                        id=self.new_answer_id(),
                        value=answer,
                    )
            qa = QuestionWithAnswer(question=question, answer=_answer)
            self._data.add(qa)
            return deepcopy(qa)

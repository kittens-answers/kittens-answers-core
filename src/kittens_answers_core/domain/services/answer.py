from typing import Mapping

from kittens_answers_core.domain.entities.entities import Answer, IDType, Question, User
from kittens_answers_core.infrastructure.repository.answer.base import AnswerNotFound

from ...infrastructure.unit_of_work.abc_uow import UoW


async def add_answer(
    uow: UoW, question_id: IDType, value: str | frozenset[str] | tuple[str, ...] | Mapping[str, str], user: User
) -> tuple[Question, Answer, bool]:
    async with uow:
        question = await uow.question_repository.get_by_id(question_id=question_id)
        try:
            answer = await uow.answer_repository.get_answer(question=question, value=value)
            is_created = False
        except AnswerNotFound:
            answer = await uow.answer_repository.create_answer(user=user, question=question, value=value)
            is_created = True
            await uow.commit()

        return (question, answer, is_created)

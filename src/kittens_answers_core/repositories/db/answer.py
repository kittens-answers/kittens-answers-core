from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from kittens_answers_core.errors import (
    AnswerAlreadyExistError,
    AnswerDoesNotExistError,
)
from kittens_answers_core.models import Answer
from kittens_answers_core.models.db_models import DBAnswer
from kittens_answers_core.repositories.base.answer import BaseAnswerRepository


class SQLAlchemyAnswerRepository(BaseAnswerRepository):
    session: AsyncSession

    async def get_by_uid(self, answer_uid: UUID) -> Answer:
        answer = await self.session.scalar(select(DBAnswer).where(DBAnswer.uid == answer_uid))
        if answer is None:
            raise AnswerDoesNotExistError
        return Answer(
            uid=answer.uid,
            creator=answer.creator_id,
            question_uid=answer.question_uid,
            answer=answer.answer,
            extra_answer=answer.extra_answer,
            is_correct=answer.is_correct,
        )

    async def get(self, answer: list[str], extra_answer: list[str], question_uid: UUID, *, is_correct: bool) -> Answer:
        _answer = await self.session.scalar(
            select(DBAnswer).where(
                DBAnswer.answer == answer,
                DBAnswer.extra_answer == extra_answer,
                DBAnswer.question_uid == question_uid,
                DBAnswer.is_correct == is_correct,
            )
        )
        if _answer is None:
            raise AnswerDoesNotExistError
        return Answer(
            uid=_answer.uid,
            creator=_answer.creator_id,
            question_uid=_answer.question_uid,
            answer=_answer.answer,
            extra_answer=_answer.extra_answer,
            is_correct=_answer.is_correct,
        )

    async def create(
        self, answer: list[str], extra_answer: list[str], question_uid: UUID, creator_id: UUID, *, is_correct: bool
    ) -> Answer:
        _answer = DBAnswer(
            uid=uuid4(),
            creator_id=creator_id,
            question_uid=question_uid,
            answer=answer,
            extra_answer=extra_answer,
            is_correct=is_correct,
        )
        self.session.add(_answer)
        try:
            await self.session.flush()
        except IntegrityError as error:
            raise AnswerAlreadyExistError from error
        return Answer(
            uid=_answer.uid,
            creator=_answer.creator_id,
            question_uid=_answer.question_uid,
            answer=_answer.answer,
            extra_answer=_answer.extra_answer,
            is_correct=_answer.is_correct,
        )

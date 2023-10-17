from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from kittens_answers_core.models import Question, QuestionTypes
from kittens_answers_core.services.base.question_services import BaseQuestionServices
from kittens_answers_core.services.db.models import DBQuestion, DBRootQuestion
from kittens_answers_core.services.db.session_mixin import SessionMixin
from kittens_answers_core.services.errors import QuestionAlreadyExistError, QuestionDoesNotExistError


class SQLAlchemyQuestionServices(BaseQuestionServices, SessionMixin):
    async def get_by_uid(self, uid: UUID) -> Question:
        question = await self.session.scalar(
            select(DBQuestion).where(DBQuestion.uid == uid).options(selectinload(DBQuestion.root_question))
        )
        if question is None:
            raise QuestionDoesNotExistError
        return Question(
            uid=question.uid,
            creator=question.creator_id,
            question_type=QuestionTypes(question.root_question.question_type),
            text=question.root_question.text,
            options=set(question.options),
            extra_options=set(question.extra_options),
        )

    async def get(
        self, question_type: QuestionTypes, question_text: str, options: set[str], extra_options: set[str]
    ) -> Question:
        root_question = await self.session.scalar(
            select(DBRootQuestion).where(
                DBRootQuestion.question_type == str(question_type), DBRootQuestion.text == question_text
            )
        )
        if root_question is None:
            raise QuestionDoesNotExistError
        question = await self.session.scalar(
            select(DBQuestion)
            .options(selectinload(DBQuestion.root_question))
            .where(
                DBQuestion.root_question_uid == root_question.root_uid,
                DBQuestion.options == sorted(options),
                DBQuestion.extra_options == sorted(extra_options),
            )
        )
        if question is None:
            raise QuestionDoesNotExistError
        return Question(
            uid=question.uid,
            creator=question.creator_id,
            question_type=QuestionTypes(question.root_question.question_type),
            text=question.root_question.text,
            options=set(question.options),
            extra_options=set(question.extra_options),
        )

    async def create(
        self,
        question_type: QuestionTypes,
        question_text: str,
        options: set[str],
        extra_options: set[str],
        creator_id: UUID,
    ) -> Question:
        root_question = await self.session.scalar(
            select(DBRootQuestion).where(
                DBRootQuestion.question_type == str(question_type), DBRootQuestion.text == question_text
            )
        )
        if root_question is None:
            root_question = DBRootQuestion(root_uid=uuid4(), question_type=str(question_type), text=question_text)
            self.session.add(root_question)
            await self.session.flush()
        question = await self.session.scalar(
            select(DBQuestion)
            .options(selectinload(DBQuestion.root_question))
            .where(
                DBQuestion.root_question_uid == root_question.root_uid,
                DBQuestion.options == sorted(options),
                DBQuestion.extra_options == sorted(extra_options),
            )
        )
        if question is not None:
            raise QuestionAlreadyExistError
        question = DBQuestion(
            uid=uuid4(),
            creator_id=creator_id,
            options=sorted(options),
            extra_options=sorted(extra_options),
            root_question_uid=root_question.root_uid,
        )
        self.session.add(question)
        await self.session.flush()
        return Question(
            uid=question.uid,
            creator=question.creator_id,
            question_type=QuestionTypes(question.root_question.question_type),
            text=question.root_question.text,
            options=set(question.options),
            extra_options=set(question.extra_options),
        )

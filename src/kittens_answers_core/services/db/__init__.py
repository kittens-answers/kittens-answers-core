from types import TracebackType
from typing import Self
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import selectinload

from kittens_answers_core.models import Question, QuestionTypes, User
from kittens_answers_core.services.base import (
    BaseQuestionServices,
    BaseUnitOfWork,
    BaseUserServices,
)
from kittens_answers_core.services.db.models import DBQuestion, DBRootQuestion, DBUser
from kittens_answers_core.services.errors import (
    QuestionAlreadyExistError,
    QuestionDoesNotExistError,
    UserAlreadyExistError,
    UserDoesNotExistError,
)


class SQLAlchemyUnitOfWork(BaseUnitOfWork):
    session: AsyncSession

    def __init__(self, db_url: str) -> None:
        self._engine = create_async_engine(url=db_url)
        self.session_factory = async_sessionmaker(bind=self._engine, expire_on_commit=False)

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def __aenter__(self) -> Self:
        self.session = AsyncSession(bind=self._engine)
        self.user_services = SQLAlchemyUserServices(session=self.session)
        self.question_services = SQLAlchemyQuestionServices(session=self.session)
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType
    ) -> bool | None:
        await super().__aexit__(exc_type, exc_value, traceback)
        await self.session.close()
        delattr(self, "user_services")
        delattr(self, "question_services")
        return None


class SQLAlchemyUserServices(BaseUserServices):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_foreign_id(self, foreign_id: str) -> User:
        user = await self.session.scalar(select(DBUser).where(DBUser.foreign_id == foreign_id))
        if user is None:
            raise UserDoesNotExistError
        return User(uid=user.uid, foreign_id=user.foreign_id)

    async def get_by_uid(self, uid: str) -> User:
        user = await self.session.scalar(select(DBUser).where(DBUser.uid == UUID(uid)))
        if user is None:
            raise UserDoesNotExistError
        return User(uid=user.uid, foreign_id=user.foreign_id)

    async def create(self, foreign_id: str) -> User:
        user = DBUser(foreign_id=foreign_id, uid=uuid4())
        self.session.add(user)
        try:
            await self.session.flush()
        except IntegrityError as error:
            raise UserAlreadyExistError from error
        return User(uid=user.uid, foreign_id=user.foreign_id)


class SQLAlchemyQuestionServices(BaseQuestionServices):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_uid(self, uid: str) -> Question:
        question = await self.session.scalar(
            select(DBQuestion).where(DBQuestion.uid == UUID(uid)).options(selectinload(DBQuestion.root_question))
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
        creator_id: str,
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
            creator_id=UUID(creator_id),
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

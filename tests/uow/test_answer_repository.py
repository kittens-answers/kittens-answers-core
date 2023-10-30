import pytest

from kittens_answers_core.services.errors import (
    AnswerAlreadyExistError,
    AnswerDoesNotExistError,
)
from tests.uow.fixture_types import AnswerDataFactory, AnswerFactory, QuestionFactory, UIDFactory, UOWTypes, UserFactory

pytestmark = pytest.mark.anyio


class TestCreate:
    async def test_if_not_in_db(
        self,
        uow: UOWTypes,
        user_factory: UserFactory,
        answer_data_factory: AnswerDataFactory,
        question_factory: QuestionFactory,
    ) -> None:
        question_in_db = await question_factory()
        user_in_db = await user_factory()
        async with uow:
            answer = await uow.answer_services.create(creator_id=user_in_db.uid, **answer_data_factory(question_in_db))
            await uow.commit()
        assert answer.question_uid == question_in_db.uid

    async def test_if_in_db(
        self,
        uow: UOWTypes,
        user_factory: UserFactory,
        answer_factory: AnswerFactory,
    ) -> None:
        user_in_db = await user_factory()
        answer_in_db = await answer_factory()
        with pytest.raises(AnswerAlreadyExistError):
            async with uow:
                await uow.answer_services.create(
                    answer=answer_in_db.answer,
                    extra_answer=answer_in_db.extra_answer,
                    question_uid=answer_in_db.question_uid,
                    creator_id=user_in_db.uid,
                    is_correct=answer_in_db.is_correct,
                )
                await uow.commit()


class TestGetByUID:
    async def test_if_not_in_db(self, uow: UOWTypes, uid_factory: UIDFactory) -> None:
        with pytest.raises(AnswerDoesNotExistError):
            async with uow:
                await uow.answer_services.get_by_uid(answer_uid=uid_factory())

    async def test_if_in_db(
        self,
        uow: UOWTypes,
        answer_factory: AnswerFactory,
    ) -> None:
        answer_in_db = await answer_factory()
        async with uow:
            answer = await uow.answer_services.get_by_uid(answer_uid=answer_in_db.uid)
        assert answer == answer_in_db


class TestGet:
    async def test_if_not_in_db(
        self,
        uow: UOWTypes,
        user_factory: UserFactory,
        answer_data_factory: AnswerDataFactory,
        question_factory: QuestionFactory,
    ) -> None:
        user = await user_factory()
        question = await question_factory(user_uid=user.uid)
        answer_data = answer_data_factory(question)
        with pytest.raises(AnswerDoesNotExistError):
            async with uow:
                await uow.answer_services.get(**answer_data)

    async def test_if_in_db(
        self,
        uow: UOWTypes,
        user_factory: UserFactory,
        answer_data_factory: AnswerDataFactory,
        question_factory: QuestionFactory,
        answer_factory: AnswerFactory,
    ) -> None:
        user = await user_factory()
        question = await question_factory(user_uid=user.uid)
        answer_data = answer_data_factory(question)
        answer_in_db = await answer_factory(answer_data=answer_data, question=question, user_uid=user.uid)

        async with uow:
            answer = await uow.answer_services.get(**answer_data)

        assert answer == answer_in_db

import pytest

from kittens_answers_core.services.errors import (
    QuestionAlreadyExistError,
    QuestionDoesNotExistError,
)
from tests.uow.fixture_types import (
    QuestionDataFactory,
    QuestionFactory,
    UIDFactory,
    UOWTypes,
    UserFactory,
)

pytestmark = pytest.mark.anyio


class TestGetByUid:
    async def test_if_not_in_db(self, uow: UOWTypes, uid_factory: UIDFactory) -> None:
        with pytest.raises(QuestionDoesNotExistError):
            async with uow:
                await uow.question_services.get_by_uid(uid=uid_factory())

    async def test_if_in_db(self, uow: UOWTypes, question_factory: QuestionFactory) -> None:
        question_in_db = await question_factory()
        async with uow:
            question = await uow.question_services.get_by_uid(uid=question_in_db.uid)
        assert question == question_in_db


class TestGet:
    async def test_if_not_in_db(self, uow: UOWTypes, question_data_factory: QuestionDataFactory) -> None:
        with pytest.raises(QuestionDoesNotExistError):
            async with uow:
                await uow.question_services.get(**question_data_factory())

    async def test_if_not_in_db_root_question(
        self, uow: UOWTypes, question_factory: QuestionFactory, question_data_factory: QuestionDataFactory
    ) -> None:
        question_in_db = await question_factory()
        with pytest.raises(QuestionDoesNotExistError):
            data = question_data_factory()
            data.update({"question_type": question_in_db.question_type, "question_text": question_in_db.text})
            async with uow:
                await uow.question_services.get(**data)

    async def test_if_in_db(self, uow: UOWTypes, question_factory: QuestionFactory) -> None:
        question_in_db = await question_factory()
        async with uow:
            question = await uow.question_services.get(
                question_type=question_in_db.question_type,
                question_text=question_in_db.text,
                options=question_in_db.options,
                extra_options=question_in_db.extra_options,
            )
        assert question_in_db == question


class TestCreate:
    async def test_if_not_in_db(
        self, uow: UOWTypes, question_data_factory: QuestionDataFactory, user_factory: UserFactory
    ) -> None:
        user_in_db = await user_factory()
        async with uow:
            question = await uow.question_services.create(creator_id=user_in_db.uid, **question_data_factory())
            await uow.commit()

        async with uow:
            assert question == (await uow.question_services.get_by_uid(question.uid))

    async def test_if_in_db(self, uow: UOWTypes, question_factory: QuestionFactory, user_factory: UserFactory) -> None:
        question_in_db = await question_factory()
        user_in_db = await user_factory()
        with pytest.raises(QuestionAlreadyExistError):
            async with uow:
                question = await uow.question_services.create(
                    question_type=question_in_db.question_type,
                    question_text=question_in_db.text,
                    options=question_in_db.options,
                    extra_options=question_in_db.extra_options,
                    creator_id=user_in_db.uid,
                )
            assert question_in_db == question

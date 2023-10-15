from collections.abc import Callable
from uuid import UUID

import pytest
from mimesis.types import JSON

from kittens_answers_core.models import Question, User
from kittens_answers_core.services.base import BaseUnitOfWork
from kittens_answers_core.services.errors import (
    QuestionAlreadyExistError,
    QuestionDoesNotExistError,
)

pytestmark = pytest.mark.anyio


class TestGetByUid:
    @pytest.mark.usefixtures("populate_questions")
    async def test_if_not_in_db(self, uow: BaseUnitOfWork, question_uid_factory: Callable[..., UUID]) -> None:
        with pytest.raises(QuestionDoesNotExistError):
            async with uow:
                await uow.question_services.get_by_uid(uid=question_uid_factory())

    async def test_if_in_db(self, uow: BaseUnitOfWork, populate_questions: list[Question]) -> None:
        async with uow:
            question = await uow.question_services.get_by_uid(uid=populate_questions[0].uid)
        assert question == populate_questions[0]


class TestGet:
    @pytest.mark.usefixtures("populate_questions")
    async def test_if_not_in_db(self, uow: BaseUnitOfWork, question_data_factory: Callable[..., JSON]) -> None:
        with pytest.raises(QuestionDoesNotExistError):
            async with uow:
                await uow.question_services.get(**question_data_factory())

    async def test_if_not_in_db_root_question(
        self, uow: BaseUnitOfWork, populate_questions: list[Question], question_data_factory: Callable[..., JSON]
    ) -> None:
        with pytest.raises(QuestionDoesNotExistError):
            question_from_db = populate_questions[0]
            data = question_data_factory()
            data.update({"question_type": question_from_db.question_type, "question_text": question_from_db.text})
            async with uow:
                await uow.question_services.get(**data)

    async def test_if_in_db(self, uow: BaseUnitOfWork, populate_questions: list[Question]) -> None:
        question_from_db = populate_questions[0]
        async with uow:
            question = await uow.question_services.get(
                question_type=question_from_db.question_type,
                question_text=question_from_db.text,
                options=question_from_db.options,
                extra_options=question_from_db.extra_options,
            )
        assert question_from_db == question


class TestCreate:
    @pytest.mark.usefixtures("populate_questions")
    async def test_if_not_in_db(
        self, uow: BaseUnitOfWork, question_data_factory: Callable[..., JSON], random_user_from_db: Callable[..., User]
    ) -> None:
        async with uow:
            question = await uow.question_services.create(
                creator_id=random_user_from_db().uid, **question_data_factory()
            )
            await uow.commit()

        async with uow:
            assert question == (await uow.question_services.get_by_uid(question.uid))

    async def test_if_in_db(
        self, uow: BaseUnitOfWork, populate_questions: list[Question], random_user_from_db: Callable[..., User]
    ) -> None:
        question_from_db = populate_questions[0]
        with pytest.raises(QuestionAlreadyExistError):
            async with uow:
                question = await uow.question_services.create(
                    question_type=question_from_db.question_type,
                    question_text=question_from_db.text,
                    options=question_from_db.options,
                    extra_options=question_from_db.extra_options,
                    creator_id=random_user_from_db().uid,
                )
            assert question_from_db == question

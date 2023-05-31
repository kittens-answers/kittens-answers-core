import pytest

from kittens_answers_core.domain.entities import Question
from kittens_answers_core.infrastructure.repository.exception import (
    QuestionAlreadyExistException,
    QuestionNotFoundException,
)
from kittens_answers_core.infrastructure.unit_of_work.abc_uow import UoW

pytestmark = pytest.mark.anyio


async def test_get_by_id_if_exist(uow: UoW, question: Question):
    async with uow:
        question_2 = await uow.question_repository.get_by_id(question_id=question.id)
        await uow.commit()
    assert question == question_2


async def test_get_by_id_if_not_exist(uow: UoW):
    async with uow:
        with pytest.raises(QuestionNotFoundException):
            await uow.question_repository.get_by_id(question_id=1)
            await uow.commit()


async def test_create_twice_with_same_user(uow: UoW, question: Question):
    async with uow:
        with pytest.raises(QuestionAlreadyExistException):
            await uow.question_repository.create(
                user_id=question.created_by,
                question_text=question.text,
                question_type=question.question_type,
                options=question.options,
                extra_options=question.extra_options,
            )
            await uow.commit()


async def test_create_twice_with_different_user(uow: UoW, question: Question):
    async with uow:
        user = await uow.user_repository.create("new user")
        await uow.commit()

    async with uow:
        with pytest.raises(QuestionAlreadyExistException):
            await uow.question_repository.create(
                user_id=user.id,
                question_text=question.text,
                question_type=question.question_type,
                options=question.options,
                extra_options=question.extra_options,
            )
            await uow.commit()

import pytest

from kittens_answers_core.domain.entities import Question, QuestionType
from kittens_answers_core.infrastructure.repository.exception import (
    QuestionAlreadyExistException,
    QuestionNotFoundException,
)
from kittens_answers_core.infrastructure.unit_of_work.abc_uow import UoW

pytestmark = pytest.mark.anyio


async def test_get_by_id_if_exist(uow: UoW, question: Question):
    async with uow:
        assert len(await uow.question_repository.list()) == 1

    async with uow:
        question_2 = await uow.question_repository.get_by_id(question_id=question.id)
        await uow.commit()
    assert question == question_2


async def test_get_by_id_if_not_exist(uow: UoW):
    async with uow:
        assert len(await uow.question_repository.list()) == 0

    async with uow:
        with pytest.raises(QuestionNotFoundException):
            await uow.question_repository.get_by_id(question_id=1)
            await uow.commit()


async def test_create_twice_with_same_user(uow: UoW, question: Question):
    async with uow:
        assert len(await uow.question_repository.list()) == 1

    async with uow:
        with pytest.raises(QuestionAlreadyExistException):
            question_2 = await uow.question_repository.create(
                user_id=question.created_by,
                question_text=question.text,
                question_type=question.question_type,
                options=question.options,
                extra_options=question.extra_options,
            )
            await uow.commit()
            assert question_2 == question

    async with uow:
        assert len(await uow.question_repository.list()) == 1


async def test_create_twice_with_different_user(uow: UoW, question: Question):
    async with uow:
        user = await uow.user_repository.create("new user")
        assert len(await uow.question_repository.list()) == 1
        await uow.commit()

    async with uow:
        with pytest.raises(QuestionAlreadyExistException):
            question_2 = await uow.question_repository.create(
                user_id=user.id,
                question_text=question.text,
                question_type=question.question_type,
                options=question.options,
                extra_options=question.extra_options,
            )
            await uow.commit()
            assert question_2 == question

    async with uow:
        assert len(await uow.question_repository.list()) == 1


async def test_get_if_not_exist(uow: UoW):
    async with uow:
        assert len(await uow.question_repository.list()) == 0

    async with uow:
        with pytest.raises(QuestionNotFoundException):
            await uow.question_repository.get(
                question_text="?", question_type=QuestionType.ONE, options=frozenset(), extra_options=frozenset()
            )
            await uow.commit()


async def test_get_if_exist(uow: UoW, question: Question):
    async with uow:
        assert len(await uow.question_repository.list()) == 1

    async with uow:
        question_2 = await uow.question_repository.get(
            question_text=question.text,
            question_type=question.question_type,
            options=question.options,
            extra_options=question.extra_options,
        )
        await uow.commit()
        assert question_2 == question


async def test_get_with_different_text(uow: UoW, question: Question):
    async with uow:
        assert len(await uow.question_repository.list()) == 1

    async with uow:
        with pytest.raises(QuestionNotFoundException):
            value = "different text"
            assert value != question.text
            await uow.question_repository.get(
                question_text=value,
                question_type=question.question_type,
                options=question.options,
                extra_options=question.extra_options,
            )
            await uow.commit()


async def test_get_with_different_type(uow: UoW, question: Question):
    async with uow:
        assert len(await uow.question_repository.list()) == 1

    async with uow:
        with pytest.raises(QuestionNotFoundException):
            value = QuestionType.MANY
            assert value != question.question_type
            await uow.question_repository.get(
                question_text=question.text,
                question_type=value,
                options=question.options,
                extra_options=question.extra_options,
            )
            await uow.commit()


async def test_get_with_different_options(uow: UoW, question: Question):
    async with uow:
        assert len(await uow.question_repository.list()) == 1

    async with uow:
        with pytest.raises(QuestionNotFoundException):
            value = frozenset(("1", "2"))
            assert value != question.options
            await uow.question_repository.get(
                question_text=question.text,
                question_type=question.question_type,
                options=value,
                extra_options=question.extra_options,
            )
            await uow.commit()


async def test_get_with_different_extra_options(uow: UoW, question: Question):
    async with uow:
        assert len(await uow.question_repository.list()) == 1

    async with uow:
        with pytest.raises(QuestionNotFoundException):
            value = frozenset(("1", "2"))
            assert value != question.extra_options
            await uow.question_repository.get(
                question_text=question.text,
                question_type=question.question_type,
                options=question.options,
                extra_options=value,
            )
            await uow.commit()

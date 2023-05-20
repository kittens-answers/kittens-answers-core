import pytest

from kittens_answers_core.domain.entities.entities import QuestionType, User
from kittens_answers_core.domain.services.question import get_or_create_question
from kittens_answers_core.domain.services.user import get_or_create
from kittens_answers_core.infrastructure.unit_of_work.abc_uow import UoW

pytestmark = pytest.mark.anyio


@pytest.fixture
async def user(uow: UoW):
    async with uow:
        user = await get_or_create("user", uow=uow)
        await uow.commit()
    return user


async def test_empty(uow: UoW, user: User):
    assert len(await uow.question_repository.list()) == 0

    async with uow:
        question = await get_or_create_question(
            user=user,
            text="?",
            question_type=QuestionType.ONE,
            options=frozenset(("1", "2")),
            extra_options=frozenset(),
            uow=uow,
        )
        await uow.commit()

    assert len(await uow.question_repository.list()) == 1

    async with uow:
        question_2 = await get_or_create_question(
            user=user,
            text="?",
            question_type=QuestionType.ONE,
            options=frozenset(("1", "2")),
            extra_options=frozenset(),
            uow=uow,
        )
        await uow.commit()

    assert len(await uow.question_repository.list()) == 1

    assert question == question_2


async def test_different_options(uow: UoW, user: User):
    assert len(await uow.question_repository.list()) == 0

    async with uow:
        question = await get_or_create_question(
            user=user,
            text="?",
            question_type=QuestionType.ONE,
            options=frozenset(("1", "2")),
            extra_options=frozenset(),
            uow=uow,
        )
        await uow.commit()

    assert len(await uow.question_repository.list()) == 1

    async with uow:
        question_2 = await get_or_create_question(
            user=user,
            text="?",
            question_type=QuestionType.ONE,
            options=frozenset(),
            extra_options=frozenset(),
            uow=uow,
        )
        await uow.commit()

    assert len(await uow.question_repository.list()) == 2

    assert question.id != question_2.id

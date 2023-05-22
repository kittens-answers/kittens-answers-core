import pytest

from kittens_answers_core.domain.entities.entities import QuestionType, User
from kittens_answers_core.infrastructure.unit_of_work.abc_uow import UoW

pytestmark = pytest.mark.anyio


async def test_create(uow: UoW, user: User):
    assert len(await uow.question_repository.list()) == 0

    async with uow:
        await uow.question_repository.create(
            user=user,
            question_text="?",
            question_type=QuestionType.ONE,
            options=frozenset(),
            extra_options=frozenset(),
            answer="1",
            is_correct=True,
        )
        await uow.commit()

    assert len(await uow.question_repository.list()) == 1

    async with uow:
        await uow.question_repository.create(
            user=user,
            question_text="?",
            question_type=QuestionType.ONE,
            options=frozenset(),
            extra_options=frozenset(),
            answer="1",
            is_correct=True,
        )
        await uow.commit()

    assert len(await uow.question_repository.list()) == 1


async def test_create_with_another_user(uow: UoW, user: User):
    assert len(await uow.question_repository.list()) == 0

    async with uow:
        qa_1 = await uow.question_repository.create(
            user=user,
            question_text="?",
            question_type=QuestionType.ONE,
            options=frozenset(),
            extra_options=frozenset(),
            answer="1",
            is_correct=True,
        )
        await uow.commit()

    assert len(await uow.question_repository.list()) == 1

    async with uow:
        user_2 = await uow.user_repository.create("another_user")
        await uow.commit()

    async with uow:
        qa_2 = await uow.question_repository.create(
            user=user_2,
            question_text="?",
            question_type=QuestionType.ONE,
            options=frozenset(),
            extra_options=frozenset(),
            answer="1",
            is_correct=True,
        )
        await uow.commit()

    assert len(await uow.question_repository.list()) == 1

    assert qa_1.question == qa_2.question
    assert qa_1.answer.id == qa_2.answer.id
    assert qa_1.answer.value == qa_2.answer.value
    assert len(qa_1.answer.marks) == 1
    assert len(qa_2.answer.marks) == 2

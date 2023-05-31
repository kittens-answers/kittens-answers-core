import pytest

from kittens_answers_core.domain.entities import Question, QuestionType, User
from kittens_answers_core.infrastructure.unit_of_work.abc_uow import UoW

pytestmark = pytest.mark.anyio


@pytest.fixture
async def user(uow: UoW) -> User:
    async with uow:
        user = await uow.user_repository.create("user_1")
        await uow.commit()
    return user


@pytest.fixture
async def question(uow: UoW, user: User) -> Question:
    async with uow:
        question = await uow.question_repository.create(
            user_id=user.id,
            question_text="?",
            question_type=QuestionType.ONE,
            options=frozenset(),
            extra_options=frozenset(),
        )
        await uow.commit()
    return question

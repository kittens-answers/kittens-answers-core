# import pytest

# from kittens_answers_core.domain.entities import QuestionType, User
# from kittens_answers_core.domain.services.question import get_or_create_question
# from kittens_answers_core.infrastructure.unit_of_work.abc_uow import UoW

# pytestmark = pytest.mark.anyio


# async def test_create(uow: UoW, user: User):
#     assert len(await uow.question_repository.list()) == 0

#     question_1, is_created_1 = await get_or_create_question(
#         user=user,
#         question_text="?",
#         question_type=QuestionType.ONE,
#         options=frozenset(),
#         extra_options=frozenset(),
#         uow=uow,
#     )

#     assert is_created_1 is True
#     assert len(await uow.question_repository.list()) == 1

#     question_2, is_created_2 = await get_or_create_question(
#         user=user,
#         question_text="?",
#         question_type=QuestionType.ONE,
#         options=frozenset(),
#         extra_options=frozenset(),
#         uow=uow,
#     )

#     assert is_created_2 is False
#     assert len(await uow.question_repository.list()) == 1

#     assert question_1 == question_2

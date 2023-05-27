from ...infrastructure.repository.question.base import (
    Question,
    QuestionNotFoundException,
    QuestionType,
    User,
)
from ...infrastructure.unit_of_work.abc_uow import UoW


async def get_or_create_question(
    uow: UoW,
    question_text: str,
    question_type: QuestionType,
    options: frozenset[str],
    extra_options: frozenset[str],
    user: User,
) -> tuple[Question, bool]:
    async with uow:
        try:
            question = await uow.question_repository.get(
                question_text=question_text, question_type=question_type, options=options, extra_options=extra_options
            )
            is_created = False

        except QuestionNotFoundException:
            question = await uow.question_repository.create(
                user=user,
                question_text=question_text,
                question_type=question_type,
                options=options,
                extra_options=extra_options,
            )
            is_created = True
            await uow.commit()

        return (question, is_created)

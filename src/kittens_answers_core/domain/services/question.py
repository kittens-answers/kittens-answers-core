from ...domain.entities.entities import Options, Question, QuestionWithoutId, User
from ...domain.entities.enums import QuestionType
from ...infrastructure.unit_of_work.abc_uow import UoW


async def get_or_create_question(
    user: User,
    text: str,
    question_type: QuestionType,
    options: frozenset[str],
    extra_options: frozenset[str],
    uow: UoW,
) -> Question:
    question_dto = QuestionWithoutId(
        created_by=user,
        text=text,
        question_type=question_type,
        options=Options(options=options, extra_options=extra_options),
    )
    return await uow.question_repository.get_or_create(dto=question_dto)

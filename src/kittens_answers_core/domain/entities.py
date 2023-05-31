from dataclasses import dataclass, field
from enum import StrEnum
from typing import Mapping, TypeAlias


class QuestionType(StrEnum):
    ONE = "ONE"
    MANY = "MANY"
    ORDER = "ORDER"
    MATCH = "MATCH"


IDType: TypeAlias = int


@dataclass(kw_only=True)
class User:
    public_id: str
    id: IDType

    def __post_init__(self):
        if not self.public_id:
            raise ValueError("public id can not be empty")

    def __hash__(self) -> int:
        return self.id


@dataclass(kw_only=True)
class Question:
    id: IDType
    created_by: IDType
    text: str
    question_type: QuestionType
    options: frozenset[str] = field(default_factory=frozenset)
    extra_options: frozenset[str] = field(default_factory=frozenset)

    def __post_init__(self):
        if not self.text:
            raise ValueError("text can not be empty")
        if not all(self.options) or not all(self.extra_options):
            raise ValueError("options or extra options can not be empty")
        match self.question_type:
            case QuestionType.ONE | QuestionType.MANY | QuestionType.ORDER:
                if self.options and len(self.options) < 2:
                    raise ValueError("options is inconsistent")
                if self.extra_options:
                    raise ValueError("options is inconsistent")
            case QuestionType.MATCH:
                if self.options and len(self.options) < 2:
                    raise ValueError("options is inconsistent")
                if self.extra_options and len(self.extra_options) < 2:
                    raise ValueError("options is inconsistent")
                if len(self.options) != len(self.extra_options):
                    raise ValueError("options is inconsistent")

    def __hash__(self) -> int:
        return tuple(
            (
                self.text,
                self.question_type,
                self.options,
                self.extra_options,
            )
        ).__hash__()


@dataclass(kw_only=True)
class BaseAnswer:
    id: IDType
    question_id: IDType
    created_by: IDType


@dataclass(kw_only=True)
class OneAnswer(BaseAnswer):
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("answer can not be empty")

    def __hash__(self) -> int:
        return self.value.__hash__()


@dataclass(kw_only=True)
class ManyAnswer(BaseAnswer):
    value: frozenset[str]

    def __post_init__(self):
        if not all(self.value):
            raise ValueError("answer can not be empty")
        if len(self.value) < 1:
            raise ValueError("many answer must be one or more long")

    def __hash__(self) -> int:
        return self.value.__hash__()


@dataclass(kw_only=True)
class OrderAnswer(BaseAnswer):
    value: tuple[str, ...]

    def __post_init__(self):
        if not all(self.value):
            raise ValueError("answer can not be empty")
        if len(self.value) < 2:
            raise ValueError("order answer must be two or more long")

    def __hash__(self) -> int:
        return self.value.__hash__()


@dataclass(kw_only=True)
class MatchAnswer(BaseAnswer):
    value: Mapping[str, str]

    def __post_init__(self):
        if not all(self.value.keys()) or not all(self.value.values()):
            raise ValueError("answer can not be empty")
        if len(self.value) < 2:
            raise ValueError("match answer must be two or more long")

    def __hash__(self) -> int:
        return self.value.__hash__()


Answer: TypeAlias = OneAnswer | ManyAnswer | OrderAnswer | MatchAnswer


@dataclass(kw_only=True)
class Mark:
    user_id: IDType
    answer_id: IDType
    is_correct: bool

    def __hash__(self) -> int:
        return tuple((self.user_id, self.answer_id)).__hash__()


# AnswerType = TypeVar("AnswerType", bound=Answer)


# @dataclass(frozen=True, kw_only=True)
# class QuestionWithAnswer(Generic[AnswerType]):
#     question: Question
#     answer: AnswerType

#     def __post_init__(self):
#         match self.question.question_type:
#             case QuestionType.ONE:
#                 if not isinstance(self.answer, OneAnswer):
#                     raise ValueError("answer is inconsistent with question type")
#                 if self.question.options and self.answer.value not in self.question.options:
#                     raise ValueError("answer is inconsistent with question options")
#             case QuestionType.MANY:
#                 if not isinstance(self.answer, ManyAnswer):
#                     raise ValueError("answer is inconsistent with question type")
#                 if self.question.options and not self.question.options.issuperset(self.answer.value):
#                     raise ValueError("answer is inconsistent with question options")
#             case QuestionType.ORDER:
#                 if not isinstance(self.answer, OrderAnswer):
#                     raise ValueError("answer is inconsistent with question type")
#                 if self.question.options and self.question.options != frozenset(self.answer.value):
#                     raise ValueError("answer is inconsistent with question options")
#             case QuestionType.MATCH:
#                 if not isinstance(self.answer, MatchAnswer):
#                     raise ValueError("answer is inconsistent with question type")
#                 if self.question.options and self.question.options != frozenset(self.answer.value.keys()):
#                     raise ValueError("answer is inconsistent with question options")
#             if self.question.extra_options and self.question.extra_options != frozenset(self.answer.value.values()):
#                     raise ValueError("answer is inconsistent with question options")

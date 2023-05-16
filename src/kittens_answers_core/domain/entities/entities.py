from dataclasses import dataclass, field
from typing import Generic, Mapping, TypeAlias, TypeVar

from kittens_answers_core.domain.entities.enums import QuestionType
from kittens_answers_core.domain.entities.mixins import (
    CreatedByMixin,
    IDMixin,
    MarkMixin,
    TimeStampMixin,
)


@dataclass(frozen=True, kw_only=True)
class User(IDMixin, TimeStampMixin):
    public_id: str

    def __post_init__(self):
        if not self.public_id:
            raise ValueError("public id can not be empty")


@dataclass(frozen=True, kw_only=True)
class Options:
    options: frozenset[str] = field(default_factory=frozenset)
    extra_options: frozenset[str] = field(default_factory=frozenset)

    def __post_init__(self):
        if not all(self.options) or not all(self.extra_options):
            raise ValueError("options or extra options can not be empty")


@dataclass(frozen=True, kw_only=True)
class Question(IDMixin, CreatedByMixin):
    text: str
    question_type: QuestionType
    options: Options

    def __post_init__(self):
        if not self.text:
            raise ValueError("text can not be empty")
        match self.question_type:
            case QuestionType.ONE | QuestionType.MANY | QuestionType.ORDER:
                if self.options.options and len(self.options.options) < 2:
                    raise ValueError("options is inconsistent")
                if self.options.extra_options:
                    raise ValueError("options is inconsistent")
            case QuestionType.MATCH:
                if self.options.options and len(self.options.options) < 2:
                    raise ValueError("options is inconsistent")
                if self.options.extra_options and len(self.options.extra_options) < 2:
                    raise ValueError("options is inconsistent")
                if len(self.options.options) != len(self.options.extra_options):
                    raise ValueError("options is inconsistent")


@dataclass(frozen=True, kw_only=True)
class Mark:
    user: User
    is_correct: bool


@dataclass(frozen=True, kw_only=True)
class OneAnswer(IDMixin, MarkMixin):
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("answer can not be empty")


@dataclass(frozen=True, kw_only=True)
class ManyAnswer(IDMixin, MarkMixin):
    value: frozenset[str]

    def __post_init__(self):
        if not all(self.value):
            raise ValueError("answer can not be empty")
        if len(self.value) < 1:
            raise ValueError("many answer must be one or more long")


@dataclass(frozen=True, kw_only=True)
class OrderAnswer(IDMixin, MarkMixin):
    value: tuple[str, ...]

    def __post_init__(self):
        if not all(self.value):
            raise ValueError("answer can not be empty")
        if len(self.value) < 2:
            raise ValueError("order answer must be two or more long")


@dataclass(frozen=True, kw_only=True)
class MatchAnswer(IDMixin, MarkMixin):
    value: Mapping[str, str]

    def __post_init__(self):
        if not all(self.value.keys()) or not all(self.value.values()):
            raise ValueError("answer can not be empty")
        if len(self.value) < 2:
            raise ValueError("match answer must be two or more long")


Answer: TypeAlias = OneAnswer | ManyAnswer | OrderAnswer | MatchAnswer

AnswerType = TypeVar("AnswerType", bound=Answer)


@dataclass(frozen=True, kw_only=True)
class QuestionWithAnswer(Generic[AnswerType]):
    question: Question
    answer: AnswerType

    def __post_init__(self):
        match self.question.question_type:
            case QuestionType.ONE:
                if not isinstance(self.answer, OneAnswer):
                    raise ValueError("answer is inconsistent with question type")
                if self.question.options.options and self.answer.value not in self.question.options.options:
                    raise ValueError("answer is inconsistent with question options")
            case QuestionType.MANY:
                if not isinstance(self.answer, ManyAnswer):
                    raise ValueError("answer is inconsistent with question type")
                if self.question.options.options and not self.question.options.options.issuperset(self.answer.value):
                    raise ValueError("answer is inconsistent with question options")
            case QuestionType.ORDER:
                if not isinstance(self.answer, OrderAnswer):
                    raise ValueError("answer is inconsistent with question type")
                if self.question.options.options and self.question.options.options != frozenset(self.answer.value):
                    raise ValueError("answer is inconsistent with question options")
            case QuestionType.MATCH:
                if not isinstance(self.answer, MatchAnswer):
                    raise ValueError("answer is inconsistent with question type")
                if self.question.options.options and self.question.options.options != frozenset(
                    self.answer.value.keys()
                ):
                    raise ValueError("answer is inconsistent with question options")
                if self.question.options.extra_options and self.question.options.extra_options != frozenset(
                    self.answer.value.values()
                ):
                    raise ValueError("answer is inconsistent with question options")

from enum import StrEnum
from typing import Final
from uuid import uuid4

from pydantic import UUID4, BaseModel, Field

MAX_FOREIGN_ID_LENGTH: Final[int] = 500
MAX_QUESTION_TEXT_LENGTH: Final[int] = 500


class QuestionTypes(StrEnum):
    ONE = "ONE"
    MANY = "MANY"
    ORDER = "ORDER"
    MATCH = "MATCH"


class User(BaseModel):
    uid: UUID4 = Field(default_factory=uuid4)
    foreign_id: str = Field(max_length=MAX_FOREIGN_ID_LENGTH)


class Question(BaseModel):
    uid: UUID4 = Field(default_factory=uuid4)
    creator: UUID4
    question_type: QuestionTypes
    text: str = Field(min_length=1, max_length=MAX_QUESTION_TEXT_LENGTH)
    options: set[str]
    extra_options: set[str]


class Answer(BaseModel):
    uid: UUID4 = Field(default_factory=uuid4)
    creator: UUID4
    question_uid: UUID4
    answer: list[str]
    extra_answer: list[str]
    is_correct: bool

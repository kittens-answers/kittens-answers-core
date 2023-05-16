from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from kittens_answers_core.domain.entities.entities import Mark, User


@dataclass(frozen=True, kw_only=True)
class IDMixin:
    id: int

    def __post_init__(self):
        if self.id < 0:
            raise ValueError("id must be positive")


@dataclass(frozen=True, kw_only=True)
class MarkMixin:
    marks: tuple["Mark"] = field(default_factory=tuple)


@dataclass(frozen=True, kw_only=True)
class CreatedByMixin:
    created_by: "User"


@dataclass(frozen=True, kw_only=True)
class TimeStampMixin:
    time_stamp: datetime

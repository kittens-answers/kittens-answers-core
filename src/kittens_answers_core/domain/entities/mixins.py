from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .entities import Mark, User


@dataclass(kw_only=True)
class IDMixin:
    id: int

    def __post_init__(self):
        if self.id < 0:
            raise ValueError("id must be positive")


@dataclass(kw_only=True)
class MarkMixin:
    marks: set["Mark"] = field(default_factory=set)


@dataclass(kw_only=True)
class CreatedByMixin:
    created_by: "User"


@dataclass(kw_only=True)
class TimeStampMixin:
    time_stamp: datetime

from typing import Final
from uuid import uuid4

from pydantic import UUID4, BaseModel, Field

MAX_FOREIGN_ID_LENGTH: Final[int] = 500


class User(BaseModel):
    uid: UUID4 = Field(default_factory=uuid4)
    foreign_id: str = Field(max_length=MAX_FOREIGN_ID_LENGTH)

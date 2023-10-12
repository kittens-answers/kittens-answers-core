from uuid import UUID

from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    ...


class User(Base):
    __tablename__ = "users"

    uid: Mapped[UUID] = mapped_column(PG_UUID(), primary_key=True)
    foreign_id: Mapped[str] = mapped_column(unique=True)

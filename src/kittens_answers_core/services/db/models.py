from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY, TEXT
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(AsyncAttrs, DeclarativeBase):
    ...


class DBUser(Base):
    __tablename__ = "users"

    uid: Mapped[UUID] = mapped_column(primary_key=True)
    foreign_id: Mapped[str] = mapped_column(unique=True)


class DBRootQuestion(Base):
    __tablename__ = "root_questions"
    __table_args__ = (UniqueConstraint("question_type", "text"),)

    root_uid: Mapped[UUID] = mapped_column(primary_key=True)
    question_type: Mapped[str] = mapped_column()
    text: Mapped[str] = mapped_column()
    questions: Mapped[list["DBQuestion"]] = relationship(back_populates="root_question")


class DBQuestion(Base):
    __tablename__ = "questions"
    __table_args__ = (UniqueConstraint("options", "extra_options", "root_question_uid"),)

    uid: Mapped[UUID] = mapped_column(primary_key=True)
    creator_id: Mapped[UUID] = mapped_column(ForeignKey("users.uid"))
    options: Mapped[list[str]] = mapped_column(ARRAY(TEXT()))
    extra_options: Mapped[list[str]] = mapped_column(ARRAY(TEXT()))
    root_question_uid: Mapped[UUID] = mapped_column(ForeignKey("root_questions.root_uid"))
    root_question: Mapped[DBRootQuestion] = relationship(back_populates="questions")


class DBAnswer(Base):
    __tablename__ = "answers"
    __table_args__ = (UniqueConstraint("question_uid", "answer", "extra_answer", "is_correct"),)

    uid: Mapped[UUID] = mapped_column(primary_key=True)
    creator_id: Mapped[UUID] = mapped_column(ForeignKey("users.uid"))
    question_uid: Mapped[UUID] = mapped_column(ForeignKey("questions.uid"))
    answer: Mapped[list[str]] = mapped_column(ARRAY(TEXT()))
    extra_answer: Mapped[list[str]] = mapped_column(ARRAY(TEXT()))
    is_correct: Mapped[bool]

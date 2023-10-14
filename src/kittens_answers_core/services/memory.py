from typing import Self, cast
from uuid import UUID, uuid4

from kittens_answers_core.models import Question, QuestionTypes, User
from kittens_answers_core.services.base import (
    BaseQuestionServices,
    BaseUnitOfWork,
    BaseUserServices,
)
from kittens_answers_core.services.errors import (
    QuestionAlreadyExistError,
    QuestionDoesNotExistError,
    UserAlreadyExistError,
    UserDoesNotExistError,
)


class MemoryUserServices(BaseUserServices):
    def __init__(self) -> None:
        self.data: list[User] = []

    async def get_by_foreign_id(self, foreign_id: str) -> User:
        for user in self.data:
            if user.foreign_id == foreign_id:
                return user
        raise UserDoesNotExistError

    async def get_by_uid(self, uid: str) -> User:
        uid_ = UUID(uid)
        for user in self.data:
            if user.uid == uid_:
                return user
        raise UserDoesNotExistError

    async def create(self, foreign_id: str) -> User:
        for user in self.data:
            if user.foreign_id == foreign_id:
                raise UserAlreadyExistError
        user = User(uid=uuid4(), foreign_id=foreign_id)
        self.data.append(user)
        return user


class MemoryQuestionServices(BaseQuestionServices):
    def __init__(self) -> None:
        self.data: list[Question] = []

    async def create(
        self,
        question_type: QuestionTypes,
        question_text: str,
        options: set[str],
        extra_options: set[str],
        creator_id: str,
    ) -> Question:
        for question in self.data:
            if (
                question.question_type == question_type
                and question.text == question_text
                and question.options == options
                and question.extra_options == extra_options
            ):
                raise QuestionAlreadyExistError
        question = Question(
            creator=UUID(creator_id),
            question_type=question_type,
            text=question_text,
            options=options,
            extra_options=extra_options,
        )
        self.data.append(question)
        return question

    async def get_by_uid(self, uid: str) -> Question:
        for question in self.data:
            if question.uid == UUID(uid):
                return question
        raise QuestionDoesNotExistError

    async def get(
        self, question_type: QuestionTypes, question_text: str, options: set[str], extra_options: set[str]
    ) -> Question:
        for question in self.data:
            if (
                question.question_type == question_type
                and question.text == question_text
                and question.options == options
                and question.extra_options == extra_options
            ):
                return question
        raise QuestionDoesNotExistError


class MemoryUnitOfWork(BaseUnitOfWork):
    def __init__(self) -> None:
        self.user_services = MemoryUserServices()
        self.question_services = MemoryQuestionServices()
        self._user_back_up: list[str] = []
        self._question_back_up: list[str] = []

    async def commit(self) -> None:
        user_services = cast(MemoryUserServices, self.user_services)
        question_services = cast(MemoryQuestionServices, self.question_services)
        self._user_back_up = [user.model_dump_json() for user in user_services.data]
        self._question_back_up = [question.model_dump_json() for question in question_services.data]

    async def rollback(self) -> None:
        user_services = cast(MemoryUserServices, self.user_services)
        question_services = cast(MemoryQuestionServices, self.question_services)
        user_services.data = [User.model_validate_json(data) for data in self._user_back_up]
        question_services.data = [Question.model_validate_json(data) for data in self._question_back_up]

    async def __aenter__(self) -> Self:
        user_services = cast(MemoryUserServices, self.user_services)
        question_services = cast(MemoryQuestionServices, self.question_services)
        self._user_back_up = [user.model_dump_json() for user in user_services.data]
        self._question_back_up = [user.model_dump_json() for user in question_services.data]
        return await super().__aenter__()

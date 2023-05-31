from copy import deepcopy
from typing import Mapping

from kittens_answers_core.domain.entities import (
    Answer,
    IDType,
    ManyAnswer,
    Mark,
    MatchAnswer,
    OneAnswer,
    OrderAnswer,
    Question,
    QuestionType,
    User,
)
from kittens_answers_core.infrastructure.repository.abstract import (
    AbstractAnswerRepository,
    AbstractMarkRepository,
    AbstractQuestionRepository,
    AbstractUserRepository,
)
from kittens_answers_core.infrastructure.repository.exception import (
    AnswerAlreadyExistException,
    AnswerNotFoundException,
    MarkAlreadyExistException,
    MarkNotExistException,
    NotingToUpdateException,
    QuestionAlreadyExistException,
    QuestionNotFoundException,
    UserAlreadyExistException,
    UserNotFoundException,
)


class MemoryUserRepository(AbstractUserRepository):
    def __init__(self) -> None:
        self._data: set[User] = set()

    def new_id(self):
        if self._data:
            return max([user.id for user in self._data]) + 1
        else:
            return 1

    async def get_by_id(self, user_id: IDType) -> User:
        for user in self._data:
            if user.id == user_id:
                return user
        raise UserNotFoundException

    async def get_by_public_id(self, public_id: str) -> User:
        for user in self._data:
            if user.public_id == public_id:
                return user
        raise UserNotFoundException

    async def create(self, public_id: str) -> User:
        try:
            user = await self.get_by_public_id(public_id=public_id)
        except UserNotFoundException:
            user = User(id=self.new_id(), public_id=public_id)
            self._data.add(user)
            return user
        raise UserAlreadyExistException

    async def list(self) -> tuple[User, ...]:
        return tuple(self._data)


class MemoryQuestionRepository(AbstractQuestionRepository):
    def __init__(self) -> None:
        self._data: set[Question] = set()

    async def list(self) -> tuple[Question, ...]:
        return tuple(self._data)

    def new_question_id(self):
        if self._data:
            return max([item.id for item in self._data]) + 1
        else:
            return 1

    async def get_by_id(self, question_id: IDType) -> Question:
        for item in self._data:
            if item.id == question_id:
                return deepcopy(item)
        raise QuestionNotFoundException

    async def create(
        self,
        user_id: IDType,
        question_text: str,
        question_type: QuestionType,
        options: frozenset[str],
        extra_options: frozenset[str],
    ) -> Question:
        question = Question(
            id=self.new_question_id(),
            created_by=user_id,
            text=question_text,
            question_type=question_type,
            options=options,
            extra_options=extra_options,
        )
        if question.__hash__() in (item.__hash__() for item in self._data):
            raise QuestionAlreadyExistException
        self._data.add(question)
        return deepcopy(question)

    async def get(
        self, question_text: str, question_type: QuestionType, options: frozenset[str], extra_options: frozenset[str]
    ) -> Question:
        for item in self._data:
            if (
                item.text == question_text
                and item.question_type == question_type
                and item.options == options
                and item.extra_options == extra_options
            ):
                return deepcopy(item)
        else:
            raise QuestionNotFoundException


class MemoryAnswerRepository(AbstractAnswerRepository):
    def __init__(self) -> None:
        self._data: set[Answer] = set()

    def new_id(self):
        if self._data:
            return max([user.id for user in self._data]) + 1
        else:
            return 1

    async def create_answer(
        self, user_id: IDType, question_id: IDType, value: str | frozenset[str] | tuple[str, ...] | Mapping[str, str]
    ) -> Answer:
        match value:
            case str():
                answer = OneAnswer(id=self.new_id(), question_id=question_id, created_by=user_id, value=value)
            case frozenset():
                answer = ManyAnswer(id=self.new_id(), question_id=question_id, created_by=user_id, value=value)
            case tuple():
                answer = OrderAnswer(id=self.new_id(), question_id=question_id, created_by=user_id, value=value)
            case Mapping():
                answer = MatchAnswer(id=self.new_id(), question_id=question_id, created_by=user_id, value=value)
            case _:
                raise ValueError

        if answer.__hash__() in (item.__hash__() for item in self._data):
            raise AnswerAlreadyExistException
        else:
            self._data.add(answer)
            return deepcopy(answer)

    async def get_answer(
        self, question_id: IDType, value: str | frozenset[str] | tuple[str, ...] | Mapping[str, str]
    ) -> Answer:
        for answer in self._data:
            if answer.question_id == question_id and answer.value == value:
                return deepcopy(answer)
        else:
            raise AnswerNotFoundException


class MemoryMarkRepository(AbstractMarkRepository):
    def __init__(self) -> None:
        self._data: set[Mark] = set()

    async def create(self, user_id: IDType, answer_id: IDType, value: bool) -> Mark:
        mark = Mark(user_id=user_id, answer_id=answer_id, is_correct=value)
        if mark.__hash__() in [item.__hash__() for item in self._data]:
            raise MarkAlreadyExistException
        else:
            self._data.add(mark)
            return deepcopy(mark)

    async def update(self, user_id: IDType, answer_id: IDType, value: bool) -> Mark:
        for item in self._data:
            if item.answer_id == answer_id and item.user_id == user_id:
                if item.is_correct == value:
                    raise NotingToUpdateException
                else:
                    item.is_correct = value
                    return deepcopy(item)
        else:
            raise MarkNotExistException

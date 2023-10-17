from typing import Generic, TypeVar

from kittens_answers_core.models import Question, User

TModel = TypeVar("TModel", User, Question)


class MemoryBackUpMixin(Generic[TModel]):
    def __init__(self, service_model: type[TModel], name: str, data: list[TModel]) -> None:
        self.model: type[TModel] = service_model
        self.data: list[TModel] = data
        self._backup: list[str] = []
        self._name = name

    @property
    def backup(self) -> list[TModel]:
        return [self.model.model_validate_json(data_entity) for data_entity in self._backup]

    @backup.setter
    def backup(self, value: list[TModel]) -> None:
        self._backup = [data_entity.model_dump_json() for data_entity in value]

    def make_backup(self) -> None:
        self.backup = self.data

    def rollback_backup(self) -> None:
        self.data = self.backup

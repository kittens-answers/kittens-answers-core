from copy import deepcopy
from typing import cast

from ..repository.memory_user import MemoryUserRepository
from .abc_uow import UoW


class MemoryUoW(UoW):
    def __init__(self) -> None:
        self.user_repository = MemoryUserRepository()

    async def __aenter__(self):
        self._old_user_data = deepcopy(cast(MemoryUserRepository, self.user_repository)._data)
        return self

    async def rollback(self):
        if hasattr(self, "_old_user_data"):
            cast(MemoryUserRepository, self.user_repository)._data = self._old_user_data

    async def commit(self):
        del self._old_user_data

import pytest

from kittens_answers_core.infrastructure.unit_of_work.abc_uow import UoW
from kittens_answers_core.infrastructure.unit_of_work.memory_uow import MemoryUoW


@pytest.fixture
def uow() -> UoW:
    return MemoryUoW()

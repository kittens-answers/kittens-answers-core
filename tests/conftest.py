from collections.abc import Generator
from typing import cast

import pytest
from testcontainers.postgres import PostgresContainer  # pyright: ignore [reportMissingTypeStubs]


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
def db_container_url() -> Generator[str, None, None]:
    with PostgresContainer(driver="psycopg") as container:
        yield cast(str, container.get_connection_url())  # pyright: ignore [reportUnknownMemberType]

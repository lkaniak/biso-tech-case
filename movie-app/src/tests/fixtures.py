from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from src.infrastructure.settings import Settings
from src.main import app

test_settings = Settings()
test_settings.POSTGRES_DB = f"{test_settings.POSTGRES_DB}_test"
test_settings.EMAIL_TEST_USER = "test@example.com"
test_settings.FIRST_SUPERUSER = "Super User"
test_settings.FIRST_SUPERUSER_PASSWORD = "test123"


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c

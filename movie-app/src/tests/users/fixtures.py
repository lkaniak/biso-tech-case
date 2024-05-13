from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete

from src.infrastructure.settings import settings
from src.infrastructure.database import engine
from src.tests.fixtures import init_test_db
from src.core.v1.users.models import User
from src.tests.users.utils import authentication_token_from_email
from src.tests.users.utils import get_superuser_token_headers


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        init_test_db(session)
        yield session
        statement = delete(User)
        session.execute(statement)
        session.commit()


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )

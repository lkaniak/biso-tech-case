from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from src.infrastructure.settings import Settings
from src.main import app
from src.core.v1.users.models import User, UserCreate
from sqlmodel import SQLModel, Session, create_engine, select
import src.core.v1.users.service as user_service


test_settings = Settings()
test_settings.POSTGRES_DB = f"{test_settings.POSTGRES_DB}_test"
test_settings.EMAIL_TEST_USER = "test@example.com"
test_settings.FIRST_SUPERUSER = "Super User"
test_settings.FIRST_SUPERUSER_PASSWORD = "test123"


def init_test_db(session: Session) -> None:

    SQLModel.metadata.create_all(
        create_engine(str(test_settings.SQLALCHEMY_DATABASE_URI))
    )

    user = session.exec(
        select(User).where(User.email == test_settings.TEST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=test_settings.EMAIL_TEST_USER,
            password=test_settings.TEST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = user_service.create_user(user_create=user_in)


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c

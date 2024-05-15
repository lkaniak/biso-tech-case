import os
from typing import Generator

from sqlmodel import Session

from api.infrastructure.database.engine import engine
from api.infrastructure.settings import settings
from api.tests.settings import test_settings

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def get_db_url():
    return str(
        test_settings.SQLALCHEMY_DATABASE_URI
        if os.getenv("ENVIRONMENT", "") == "staging"
        else settings.SQLALCHEMY_DATABASE_URI
    )

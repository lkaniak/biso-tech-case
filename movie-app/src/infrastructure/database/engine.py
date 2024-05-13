import os

from sqlalchemy import create_engine

from src.infrastructure.settings import settings
from src.tests.fixtures import test_settings

engine = create_engine(
    str(
        test_settings.SQLALCHEMY_DATABASE_URI
        if os.getenv("ENVIRONMENT", "") == "staging"
        else settings.SQLALCHEMY_DATABASE_URI
    )
)

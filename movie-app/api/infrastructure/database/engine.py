import os

from sqlalchemy import create_engine

from api.infrastructure.settings import settings
from api.tests.settings import test_settings

engine = create_engine(
    str(
        test_settings.SQLALCHEMY_DATABASE_URI
        if os.getenv("ENVIRONMENT", "") == "staging"
        else settings.SQLALCHEMY_DATABASE_URI
    )
)

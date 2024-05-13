import os

from src.infrastructure.settings import Settings

test_settings = Settings()
test_settings.POSTGRES_DB = f"{test_settings.POSTGRES_DB}_test"
test_settings.EMAIL_TEST_USER = (
    "test@example.com"
    if os.getenv("EMAIL_TEST_USER") is None
    else os.getenv("EMAIL_TEST_USER")
)
test_settings.FIRST_SUPERUSER = (
    "Super User" if os.getenv("FIRST_SUPERUSER") is None else os.getenv("FIRST_SUPERUSER")
)
test_settings.FIRST_SUPERUSER_PASSWORD = (
    "test123"
    if os.getenv("FIRST_SUPERUSER_PASSWORD") is None
    else os.getenv("FIRST_SUPERUSER_PASSWORD")
)

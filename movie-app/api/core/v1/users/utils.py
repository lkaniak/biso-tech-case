from fastapi import Depends
from sqlalchemy import create_engine
from sqlmodel import select, SQLModel, Session

from src.core.v1.users.models import User, UserCreate
from src.infrastructure.database.engine import engine
from src.infrastructure.security import get_password_hash
from src.infrastructure.settings import settings
from src.core.v1.users.service import create_user
from src.infrastructure.database.session import db_session
from src.tests.settings import test_settings


def init_db_users() -> None:
    with Session(engine) as session:
        db_session.set(session)
        user = session.exec(
            select(User).where(User.email == settings.EMAIL_FIRST_SUPERUSER)
        ).first()
        if not user:
            user_in = UserCreate(
                email=settings.EMAIL_FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                nickname=settings.FIRST_SUPERUSER_NICKNAME,
                hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
                is_superuser=True,
            )
            user = create_user(user_create=user_in)


def init_test_db() -> None:
    with Session(engine) as session:
        db_session.set(session)
        user = session.exec(
            select(User).where(User.email == test_settings.EMAIL_TEST_USER)
        ).first()
        if not user:
            print(f"test_settings: {test_settings}")
            user_in = UserCreate(
                email=test_settings.EMAIL_TEST_USER,
                password=test_settings.FIRST_SUPERUSER_PASSWORD,
                nickname=test_settings.FIRST_SUPERUSER_NICKNAME,
                hashed_password=get_password_hash(
                    test_settings.FIRST_SUPERUSER_PASSWORD
                ),
                is_superuser=True,
            )
            user = create_user(user_create=user_in)

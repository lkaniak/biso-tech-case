import names
from sqlmodel import select, insert, Session

from api.core.v1.users.models import User, UserCreate
from api.infrastructure.database.engine import engine
from api.infrastructure.security import get_password_hash
from api.infrastructure.settings import settings
from api.core.v1.users.service import create_user
from api.infrastructure.database.session import db_session
from api.lib.utils import random_email, random_lower_string, random_nickname
from api.tests.settings import test_settings


def generate_user() -> UserCreate:
    email = random_email()
    password = random_lower_string()
    nickname = random_nickname()
    full_name = names.get_full_name()
    return UserCreate(
        email=email,
        password=password,
        nickname=nickname,
        full_name=full_name,
    )


def populate_users(session: Session, qtd: int, users_limit: int = 50):
    users = session.exec(select(User)).all()
    if not len(users) > users_limit:
        generated_users = [generate_user() for x in range(0, qtd + 1)]
        session.execute(insert(User), generated_users)
        session.commit()


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
        populate_users(session=session, qtd=50)


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

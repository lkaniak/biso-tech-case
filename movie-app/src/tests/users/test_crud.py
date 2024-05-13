from fastapi.encoders import jsonable_encoder
from sqlmodel import Session

from src.core.v1.users.models import UserCreate, UserUpdate, User
from src.infrastructure.security import verify_password
from src.lib.utils import random_email, random_lower_string
import src.core.v1.users.service as user_service
import src.core.v1.auth.service as login_service
from src.tests.fixtures import test_settings


def authenticate_user(db: Session) -> User:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = user_service.create_user(session=db, user_create=user_in)
    authenticated_user = login_service.authenticate(
        session=db, email=email, password=password
    )
    assert authenticated_user
    assert user.email == authenticated_user.email
    return authenticated_user


def get_user(db: Session, user_id: int, user_email: str) -> list[User]:
    user_1 = user_service.get_by_id(session=db, user_id=user_id)
    user_2 = user_service.get_user_by_email(session=db, email=user_email)
    assert user_2
    assert user_1.email == user_2.email
    assert jsonable_encoder(user_1) == jsonable_encoder(user_2)
    return [user_1, user_2]


def create_update_user(db: Session) -> User:
    password = random_lower_string()
    email = random_email()
    user_in = UserCreate(email=email, password=password, is_superuser=True)
    user = user_service.create_user(session=db, user_create=user_in)
    new_password = random_lower_string()
    user_in_update = UserUpdate(password=new_password, is_superuser=True)
    if user.id is not None:
        user_service.update_user(session=db, user_in=user_in_update)
    user_2 = db.get(User, user.id)
    assert user_2
    assert user.email == user_2.email
    assert verify_password(new_password, user_2.hashed_password)
    return user


def test_not_authenticate_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user = login_service.authenticate(session=db, email=email, password=password)
    assert user is None


def delete_user(db: Session, user_id: int):
    user_service.delete_user(session=db, user_id=user_id)
    user = user_service.get_by_id(session=db, user_id=user_id)
    assert user is None


def test_crud(db: Session):
    auth_user = authenticate_user(db=db)
    created_user = create_update_user(db=db)
    users = get_user(
        db=db, user_id=auth_user.id, user_email=test_settings.EMAIL_TEST_USER
    )
    delete_user(db=db, user_id=created_user.id)

from fastapi.encoders import jsonable_encoder
from sqlmodel import Session

from src.core.v1.users.models import UserCreate, UserUpdate, User
from src.infrastructure.security import verify_password
from src.lib.utils import random_email, random_lower_string, random_nickname
import src.core.v1.users.service as user_service
import src.core.v1.auth.service as login_service
from src.tests.fixtures import db
from src.tests.settings import test_settings


def authenticate_user(db) -> User:
    email = random_email()
    password = random_lower_string()
    nickname = random_nickname()
    user_in = UserCreate(email=email, password=password, nickname=nickname)
    user = user_service.create_user(user_create=user_in)
    authenticated_user = login_service.authenticate(email=email, password=password)
    assert authenticated_user
    assert user.email == authenticated_user.email
    return authenticated_user


def get_user(db, user_id: int, user_email: str) -> list[User]:
    user_1 = user_service.get_by_id(user_id=user_id)
    user_2 = user_service.get_user_by_email(email=user_email)
    assert user_2
    assert user_1.email == user_2.email
    assert jsonable_encoder(user_1) == jsonable_encoder(user_2)
    return [user_1, user_2]


def update_user(db, user: User) -> User:
    assert user.id
    new_password = random_lower_string()
    user_in_update = UserUpdate(password=new_password, is_superuser=True)
    user_service.update_user(user_in=user_in_update, user_id=user.id)
    user_2 = db.get(User, user.id)
    assert user_2
    assert user.email == user_2.email
    assert verify_password(new_password, user_2.hashed_password)
    return user


def delete_user(db, user_id: int):
    user_service.delete_user(user_id=user_id)
    user = user_service.get_by_id(user_id=user_id)
    assert user is None


def test_not_authenticate_user(db) -> None:
    email = random_email()
    password = random_lower_string()
    user = login_service.authenticate(email=email, password=password)
    assert user is None


def test_crud(db: Session):
    auth_user = authenticate_user(db=db)
    created_user = update_user(db=db, user=auth_user)
    users = get_user(db=db, user_id=auth_user.id, user_email=auth_user.email)
    delete_user(db=db, user_id=created_user.id)

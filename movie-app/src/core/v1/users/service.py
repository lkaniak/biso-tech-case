from sqlmodel import col, delete, func, select
from src.lib.models import ListData
from typing import Any
from src.infrastructure.database import SessionDep
from models import (
    Item,
    Message,
    UpdatePassword,
    User,
    UserCreate,
    UserPublic,
    UserRegister,
    UsersPublic,
    UserUpdate,
    UserUpdateMe,
)

from src.core.v1.auth.deps import CurrentUser
from src.infrastructure.security import get_password_hash


def get_by_id(session: SessionDep, user_id: int):
    return session.get(User, user_id)


def list_users(session: SessionDep, skip=0, limit=100):
    count_statement = select(func.count()).select_from(User)
    count = session.exec(count_statement).one()

    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()

    return ListData(count=count, data=users)


def create_user(*, session: SessionDep, user_create: UserCreate) -> User:
    valid_user_create = UserCreate.model_validate(user_create)
    db_obj = User.model_validate(
        valid_user_create,
        update={"hashed_password": get_password_hash(valid_user_create.password)},
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: SessionDep, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user = session.get(User, user_in.user_id)
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def update_me_user(
    *, session: SessionDep, user_in: UserUpdate, current_user: CurrentUser
) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    current_user.sqlmodel_update(user_data)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user


def delete_user(*, session: SessionDep, user_id: int):
    user = session.get(User, user_id)
    statement = delete(User).where(User.owner_id == user_id)
    session.exec(statement)  # type: ignore
    session.delete(user)
    session.commit()


def get_user_by_email(*, session: SessionDep, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user

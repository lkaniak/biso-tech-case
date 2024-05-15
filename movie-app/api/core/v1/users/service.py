from api.infrastructure.database.engine import engine
from sqlmodel import Session, delete, func, select

from api.lib.models import ListData, User
from typing import Any
from api.core.v1.users.models import (
    UserCreate,
    UserUpdate,
)

from api.infrastructure.security import get_password_hash
from api.infrastructure.database.session import db_session


def list_users(skip=0, limit=100):
    with Session(engine) as session:
        count_statement = select(func.count()).select_from(User)
        count = session.exec(count_statement).one()

        statement = select(User).offset(skip).limit(limit)
        users = session.exec(statement).all()

        return ListData(count=count, data=users)


def create_user(*, user_create: UserCreate) -> User:
    with Session(engine) as session:
        valid_user_create = UserCreate.model_validate(user_create)
        db_obj = User.model_validate(
            valid_user_create,
            update={"hashed_password": get_password_hash(valid_user_create.password)},
        )
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj


def update_user(*, user_id: int, user_in: UserUpdate) -> Any:
    with Session(engine) as session:
        user_data = user_in.model_dump(exclude_unset=True)
        extra_data = {}
        if "password" in user_data:
            password = user_data["password"]
            hashed_password = get_password_hash(password)
            extra_data["hashed_password"] = hashed_password
        db_user = session.get(User, user_id)
        db_user.sqlmodel_update(user_data, update=extra_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


def update_me_user(*, user_in: UserUpdate, current_user: User) -> Any:
    with Session(engine) as session:
        user_data = user_in.model_dump(exclude_unset=True)
        current_user.sqlmodel_update(user_data)
        session.add(current_user)
        session.commit()
        session.refresh(current_user)
        return current_user


def delete_user(*, user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        statement = select(User).where(User.id == user_id)
        session.exec(statement)  # type: ignore
        session.delete(user)
        session.commit()


def get_by_id(user_id: int):
    with Session(engine) as session:
        return session.get(User, user_id)


def get_user_by_email(*, email: str) -> User | None:
    with Session(engine) as session:
        statement = select(User).where(User.email == email)
        session_user = session.exec(statement).first()
        return session_user

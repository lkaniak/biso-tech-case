from api.infrastructure.database.engine import engine
from fastapi import Depends, HTTPException

import api.core.v1.users.service as user_service
from api.core.v1.auth.exceptions import InactiveUser
from api.core.v1.users.exceptions import (
    UserNotFound,
    EmailAlreadyExists,
    InvalidPassword,
    InvalidNewPassword,
    RegistrationNotSupported,
    SelfDeleteError,
)
from api.infrastructure.database.session import db_session
from api.infrastructure.security import verify_password
from api.infrastructure.settings import settings
from api.core.v1.auth.deps import decode_access_token
from api.core.v1.users.models import (
    UserCreate,
    UserRegister,
    UserUpdate,
)
from api.lib.models import User
from sqlmodel import Session


def get_current_user(sub: str = Depends(decode_access_token)) -> User:
    user = user_service.get_user_by_email(email=sub)
    if not user:
        raise UserNotFound()
    if not user.is_active:
        raise InactiveUser()
    return user


def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="O usuário não tem privilégios suficientes"
        )
    return current_user


def valid_user_id(
    user_id: int,
    current_user: User = Depends(get_current_active_superuser),
) -> User:
    user = user_service.get_by_id(user_id)
    if not user:
        raise UserNotFound()

    return user


def valid_user_create(user_create: UserCreate) -> UserCreate:
    existing_user_email(user_create.email)
    valid_password(
        new_password=user_create.new_password,
    )
    return user_create


def allow_open_registration(user_in: UserRegister) -> UserCreate:
    if not settings.USERS_OPEN_REGISTRATION:
        raise RegistrationNotSupported()
    return valid_user_create(user_in)


def existing_user_email(user_email: str):
    user = user_service.get_user_by_email(email=user_email)
    if user:
        raise EmailAlreadyExists()


def valid_password(new_password: str, current_password: str = ""):
    pass_errors: list[str] = []
    if current_password == new_password:
        pass_errors.append("Nova senha não pode ser a mesma da atual")

    if len(pass_errors) > 0:
        raise InvalidNewPassword(errors=pass_errors)


def valid_password_update(current_password: str, new_password: str, current_user: User):
    if not verify_password(current_password, current_user.hashed_password):
        raise InvalidPassword()
    valid_password(new_password=new_password, current_password=current_password)


def valid_user_delete(
    user_id: int, current_user: User = Depends(get_current_user)
) -> User:
    user = valid_user_id(user_id)
    if user == current_user:
        raise SelfDeleteError()
    return current_user


def valid_user_update(
    user_id: int, user_update: UserUpdate, current_user: User
) -> UserUpdate:
    if user_id:
        user_update.user_id = user_id
    valid_user_id(user_update.user_id)
    existing_user_email(user_update.email)
    valid_password_update(
        current_password=user_update.current_password,
        new_password=user_update.new_password,
        current_user=current_user,
    )
    return user_update

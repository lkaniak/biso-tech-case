from fastapi import Depends

import src.core.v1.users.service as user_service
from src.core.v1.users.exceptions import (
    UserNotFound,
    EmailAlreadyExists,
    InvalidPassword,
    InvalidNewPassword,
    RegistrationNotSupported,
)
from typing import Mapping
from src.infrastructure.security import verify_password
from src.infrastructure.settings import settings
from src.core.v1.auth.deps import CurrentUser, get_current_active_superuser
from src.core.v1.users.models import (
    User,
    UserCreate,
    UserPublic,
    UserRegister,
    UsersPublic,
    UserUpdate,
    UserUpdateMe,
)


async def valid_user_id(
    user_id: int, current_user: CurrentUser = Depends(get_current_active_superuser)
) -> User:
    user = await user_service.get_by_id(user_id)
    if not user:
        raise UserNotFound()

    return user


async def valid_user_create(user_create: UserCreate) -> Mapping:
    await existing_user_email(user_create.email)
    await valid_password(
        new_password=user_create.new_password,
    )
    return user_create


async def allow_open_registration(user_in: UserRegister):
    if not settings.USERS_OPEN_REGISTRATION:
        raise RegistrationNotSupported()
    await valid_user_create(user_in)


async def existing_user_email(user_email: str):
    user = await user_service.get_user_by_email(email=user_email)
    if user:
        raise EmailAlreadyExists()


async def valid_password(new_password: str, current_password: str = ""):
    pass_errors: list[str] = []
    if current_password == new_password:
        pass_errors.append("Nova senha não pode ser a mesma da atual")

    if len(pass_errors) > 0:
        raise InvalidNewPassword(errors=pass_errors)


async def valid_password_update(
    current_password: str, new_password: str, current_user: CurrentUser
):
    if not verify_password(current_password, current_user.hashed_password):
        raise InvalidPassword()
    await valid_password(new_password=new_password, current_password=current_password)


async def valid_user_delete(user_id: int) -> CurrentUser:
    current_user = CurrentUser
    user = await valid_user_id(user_id)
    if user == current_user:
        raise SelfDeleteError()
    return current_user


async def valid_user_update(
    user_id: int, user_update: UserUpdate, current_user: CurrentUser
) -> UserUpdate:
    if user_id:
        user_update.user_id = user_id
    await valid_user_id(user_update.user_id)
    await existing_user_email(user_update.email)
    await valid_password_update(
        current_password=user_update.current_password,
        new_password=user_update.new_password,
        current_user=current_user,
    )
    return user_update

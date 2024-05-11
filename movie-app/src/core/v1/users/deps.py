import src.core.v1.users.service as user_service
from src.core.v1.users.exceptions import UserNotFound, EmailAlreadyExists
from typing import Mapping
from src.core.v1.users.models import (
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


async def valid_user_id(user_id: int) -> Mapping:
    post = await user_service.get_by_id(user_id)
    if not post:
        raise UserNotFound()

    return post


async def existing_user_email(user_email: str) -> Mapping:
    user = await user_service.get_user_by_email(user_email)
    if user:
        raise EmailAlreadyExists()

    return None


async def valid_user_update(user_create: UserCreate) -> Mapping:
    try:
        await existing_user_email(user_create.email)
    except EmailAlreadyExists as e:
        raise e

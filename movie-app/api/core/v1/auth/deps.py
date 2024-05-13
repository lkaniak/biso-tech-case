from pydantic import ValidationError

import src.core.v1.auth.service as auth_service

from fastapi.security import OAuth2PasswordRequestForm

from src.core.v1.auth.exceptions import InvalidCredentials, InactiveUser
from src.core.v1.auth.models import TokenPayload
from src.core.v1.users.models import User

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from src.infrastructure.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def decode_access_token(token: str = Depends(oauth2_scheme)) -> dict:

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms="HS256",
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise InvalidCredentials()

    return token_data.sub


async def decode_refresh_token(token: str = Depends(oauth2_scheme)) -> dict:

    try:
        payload = jwt.decode(
            token,
            settings.REFRESH_SECRET_KEY,
            algorithms="HS256",
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise InvalidCredentials()

    return token_data.sub


async def valid_authentication(
    form_data: [OAuth2PasswordRequestForm, Depends()]
) -> User:
    user = await auth_service.authenticate(
        email=form_data.username, password=form_data.password
    )
    if not user:
        raise InvalidCredentials()
    elif not user.is_active:
        raise InactiveUser()
    return user

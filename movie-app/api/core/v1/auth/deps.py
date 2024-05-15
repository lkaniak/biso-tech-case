from pydantic import ValidationError

import api.core.v1.auth.service as auth_service

from fastapi.security import OAuth2PasswordRequestForm

from api.core.v1.auth.exceptions import InvalidCredentials, InactiveUser
from api.core.v1.auth.models import TokenPayload
from api.lib.models import User

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from api.infrastructure.settings import settings
from sqlmodel import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/token")


def decode_access_token(token: str = Depends(oauth2_scheme)) -> dict:

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms="HS256",
        )
        return payload["sub"]
    except (JWTError, ValidationError):
        raise InvalidCredentials()


def decode_refresh_token(token: str = Depends(oauth2_scheme)) -> dict:

    try:
        payload = jwt.decode(
            token,
            settings.REFRESH_SECRET_KEY,
            algorithms="HS256",
        )
        return payload["sub"]
    except (JWTError, ValidationError):
        raise InvalidCredentials()


def valid_authentication(form_data: OAuth2PasswordRequestForm) -> User:
    user = auth_service.authenticate(
        email=form_data.username, password=form_data.password
    )
    if not user:
        raise InvalidCredentials()
    elif not user.is_active:
        raise InactiveUser()
    return user

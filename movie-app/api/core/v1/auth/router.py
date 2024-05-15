from typing import Annotated

from api.infrastructure.database.utils import get_db
from fastapi import APIRouter, Depends
from api.lib.models import User
from api.core.v1.auth.deps import valid_authentication, decode_refresh_token
from api.core.v1.users.service import get_user_by_email
from api.infrastructure import security
from api.infrastructure.settings import settings
from api.core.v1.auth.models import Token
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

router = APIRouter()


@router.post("/login/token")
def login_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """
    Gerar token OAuth2 (JWT)
    """
    user = valid_authentication(form_data)
    access_token = security.create_access_token(
        user=user, token_type="access", ttl=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    refresh_token = security.create_access_token(
        user=user, token_type="access", ttl=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


@router.post("/login/token/refresh")
def login_access_token(token: dict = Depends(decode_refresh_token)) -> Token:
    """
    Dar refresh no token OAuth2 (JWT)
    """
    user = get_user_by_email(email=token.get["sub"])
    access_token = security.create_access_token(
        user=user, token_type="access", ttl=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    refresh_token = security.create_access_token(
        user=user, token_type="access", ttl=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )

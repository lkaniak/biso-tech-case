from typing import Annotated

from fastapi import APIRouter, Depends
from api.core.v1.users.models import User
from api.core.v1.auth.deps import valid_authentication, decode_refresh_token
from api.core.v1.users.service import get_user_by_email
from api.infrastructure import security
from api.infrastructure.settings import settings
from api.core.v1.auth.models import Token

router = APIRouter()


@router.post("/login/token")
def login_access_token(
    user: User = Annotated[User, Depends(valid_authentication)]
) -> Token:
    """
    Gerar token OAuth2 (JWT)
    """
    access_token = security.create_access_token(
        user=user, token_type="access", ttl=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    refresh_token = security.create_access_token(
        user=user, token_type="access", ttl=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


@router.post("/login/token")
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

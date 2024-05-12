from datetime import timedelta

from fastapi import APIRouter, Depends
from src.core.v1.users.models import User
from src.core.v1.auth.deps import valid_authentication
from src.infrastructure import security
from src.infrastructure.settings import settings
from src.core.v1.auth.models import Token

router = APIRouter()


@router.post("/login/access-token")
def login_access_token(user: User = Depends(valid_authentication)) -> Token:
    """
    Gerar token OAuth2 (JWT)
    """

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )

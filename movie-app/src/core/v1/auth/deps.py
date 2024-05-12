import src.core.v1.auth.service as auth_service
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import ValidationError

from src.core.v1.auth.exceptions import InvalidCredentials, InactiveUser
from src.core.v1.users.exceptions import UserNotFound
from src.infrastructure import security
from src.infrastructure.settings import settings
from src.infrastructure.database import SessionDep
from src.core.v1.auth.models import TokenPayload
from src.core.v1.users.models import User

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise InvalidCredentials()
    user = session.get(User, token_data.sub)
    if not user:
        raise UserNotFound()
    if not user.is_active:
        raise InactiveUser()
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user


async def valid_authentication(form_data: [OAuth2PasswordRequestForm, Depends()]):
    user = await auth_service.authenticate(
        email=form_data.username, password=form_data.password
    )
    if not user:
        raise InvalidCredentials()
    elif not user.is_active:
        raise InactiveUser()
    return user

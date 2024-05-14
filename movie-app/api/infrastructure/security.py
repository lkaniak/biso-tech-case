from datetime import datetime, timedelta
from typing import Literal

from jose import jwt
from passlib.context import CryptContext

from api.lib.models import User
from api.infrastructure.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_access_token(
    user: User, token_type: Literal["refresh", "access"], ttl: int
) -> str:
    # This function generates token with any claims you want

    payload = {
        "sub": user.email,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=ttl),
        "user_role": user.role,
    }

    if token_type == "access":
        key = settings.SECRET_KEY
    elif token_type == "refresh":
        key = settings.REFRESH_SECRET_KEY

    encoded_jwt = jwt.encode(payload, key, "HS256")

    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

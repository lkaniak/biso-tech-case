import api.core.v1.users.service as user_service
from api.infrastructure.database.engine import engine
from api.lib.models import User
from api.infrastructure.security import verify_password
from sqlmodel import Session


def authenticate(*, email: str, password: str) -> User | None:
    user = user_service.get_user_by_email(email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

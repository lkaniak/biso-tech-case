import src.core.v1.users.service as user_service
from src.core.v1.users.models import User
from src.infrastructure.security import verify_password


async def authenticate(*, email: str, password: str) -> User | None:
    user = await user_service.get_user_by_email(email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

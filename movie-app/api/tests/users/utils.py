from sqlmodel import Session

from api.core.v1.users.models import UserCreate, UserUpdate
from api.infrastructure.settings import settings
from fastapi.testclient import TestClient
import api.core.v1.users.service as user_service
from api.lib.utils import random_lower_string
from api.tests.fixtures import db


def user_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> dict[str, str]:
    data = {"username": email, "password": password}

    r = client.post(f"{settings.API_V1_STR}/login/token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def get_superuser_token_headers(client: TestClient) -> dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


def authentication_token_from_email(
    *, client: TestClient, email: str, db
) -> dict[str, str]:
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user = user_service.get_user_by_email(email=email)

    if not user:
        user_in_create = UserCreate(email=email, password=password)
        user = user_service.create_user(user_create=user_in_create)
    else:
        user_in_update = UserUpdate(password=password)
        if not user.id:
            raise Exception("User id not set")
        user = user_service.update_user(user_in=user_in_update, user_id=user.id)

    return user_authentication_headers(client=client, email=email, password=password)

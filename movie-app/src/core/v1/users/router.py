from fastapi import APIRouter, Depends, HTTPException
from typing import Mapping
from src.core.v1.users.deps import (
    valid_user_id,
    valid_user_update,
    valid_user_create,
    allow_open_registration,
    valid_user_delete,
)
from src.core.v1.ratings.schemas import Rating
import src.core.v1.users.service as user_service

from src.core.v1.auth.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from src.core.v1.users.models import (
    User,
    UserCreate,
    UserPublic,
    UserRegister,
    UsersPublic,
    UserUpdate,
    UserUpdateMe,
)

router = APIRouter()


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UsersPublic,
)
def read_users(skip: int = 0, limit: int = 100) -> UsersPublic:
    """
    Listar usuarios
    """

    list_data = user_service.list_users(skip=skip, limit=limit)

    return UsersPublic(data=list_data.data, count=list_data.count)


@router.post(
    "/", dependencies=[Depends(get_current_active_superuser)], response_model=UserPublic
)
def create_user(*, user_in: Depends(valid_user_create)) -> User:
    """
    Criar usuario
    """
    user = user_service.create_user(user_create=user_in)
    return user


@router.patch("/me", response_model=UserPublic)
def update_user_me(
    *, user_in: Mapping = Depends(valid_user_update), current_user: CurrentUser
):
    """
    Atualizar o próprio usuário.
    """
    user = user_service.update_me_user(current_user=current_user, user_in=user_in)
    return user


@router.get("/me", response_model=UserPublic)
def read_user_me(current_user: CurrentUser):
    """
    Get no usuario logado.
    """
    return current_user


@router.post("/signup", response_model=UserPublic)
def register_user(user_in: Depends(allow_open_registration)):
    """
    Criar usuário sem login
    """
    user = user_service.create_user(user_create=user_in)
    return user


@router.get("/{user_id}", response_model=UserPublic)
def read_user_by_id(
    user: Depends(valid_user_id),
):
    """
    Obter usuário por id.
    """
    return user


@router.patch(
    "/{user_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserPublic,
)
def update_user(
    *,
    session: SessionDep,
    user_in: UserUpdate = Depends(valid_user_update),
):
    """
    Update em um usuário por id.
    """

    db_user = user_service.update_user(session=session, user_in=user_in)
    return db_user


@router.delete("/{user_id}", dependencies=[Depends(get_current_active_superuser)])
def delete_user(
    session: SessionDep,
    user_id: int,
    current_user: CurrentUser = Depends(valid_user_delete),
) -> Message:
    """
    Remover um usuário por id.
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user == current_user:
        raise HTTPException(
            status_code=403, detail="Super users are not allowed to delete themselves"
        )
    return Message(message="User deleted successfully")


# @router.get("/{user_id}/ratings", response_model=list[Rating])
# async def get_user_ratings(user: Mapping = Depends(valid_user_id)):
#     ratings = await service.get_ratings(user["id"])
#
#     return ratings

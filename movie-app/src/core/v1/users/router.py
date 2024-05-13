from typing import Annotated

from fastapi import APIRouter, Depends
from src.core.v1.users.deps import (
    valid_user_id,
    valid_user_update,
    valid_user_create,
    allow_open_registration,
    valid_user_delete,
    get_current_user,
)
from src.core.v1.ratings.schemas import Rating
import src.core.v1.users.service as user_service
from src.core.v1.users.deps import (
    get_current_active_superuser,
)
from src.core.v1.users.models import (
    User,
    UserPublic,
    UsersPublic,
    UserUpdate,
    UserCreate,
)
from src.lib.models import Message

router = APIRouter()


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UsersPublic,
)
def read_users(
    skip: int = 0, limit: int = 100, current_user: User = Depends(get_current_user)
) -> UsersPublic:
    """
    Listar usuarios
    """

    list_data = user_service.list_users(skip=skip, limit=limit)

    return UsersPublic(data=list_data.data, count=list_data.count)


@router.post(
    "/", dependencies=[Depends(get_current_active_superuser)], response_model=UserPublic
)
def create_user(
    *,
    user_in: Annotated[UserCreate, Depends(valid_user_create)],
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Criar usuario
    """
    user = user_service.create_user(user_create=user_in)
    return user


@router.patch("/me", response_model=UserPublic)
def update_user_me(
    *,
    user_in: UserUpdate = Depends(valid_user_update),
    current_user: User = Depends(get_current_user),
):
    """
    Atualizar o próprio usuário.
    """
    user = user_service.update_me_user(current_user=current_user, user_in=user_in)
    return user


@router.get("/me", response_model=UserPublic)
def read_user_me(current_user: User = Depends(get_current_user)):
    """
    Get no usuario logado.
    """
    return current_user


@router.post("/signup", response_model=UserPublic)
def register_user(user_in: Annotated[UserCreate, Depends(allow_open_registration)]):
    """
    Criar usuário sem login
    """
    user = user_service.create_user(user_create=user_in)
    return user


@router.get("/{user_id}", response_model=UserPublic)
def read_user_by_id(
    user: Annotated[User, Depends(valid_user_id)],
    current_user: User = Depends(get_current_user),
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
    user_in: UserUpdate = Depends(valid_user_update),
    user_id: int,
    current_user: User = Depends(get_current_user),
):
    """
    Update em um usuário por id.
    """

    db_user = user_service.update_user(user_in=user_in, user_id=user_id)
    return db_user


@router.delete("/{user_id}", dependencies=[Depends(get_current_active_superuser)])
def delete_user(
    user_id: int,
    current_user: User = Depends(valid_user_delete),
) -> Message:
    """
    Remover um usuário por id.
    """
    user_service.delete_user(user_id=user_id)
    return Message(message="Usuario removido com sucesso")


# @router.get("/{user_id}/ratings", response_model=list[Rating])
# async def get_user_ratings(user: Mapping = Depends(valid_user_id)):
#     ratings = await service.get_ratings(user["id"])
#
#     return ratings

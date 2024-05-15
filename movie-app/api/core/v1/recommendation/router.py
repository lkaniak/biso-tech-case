from typing import Annotated

from api.core.v1.recommendation.schemas import NewUserRatings, Recommendations
from fastapi import APIRouter, Depends
from api.core.v1.users.deps import (
    valid_user_id,
    get_current_user,
)
from api.lib.models import Message, User

import api.core.v1.recommendation.service as recommendation_service

router = APIRouter()


@router.post("/", response_model=list[Recommendations])
def create_recommendation(
    *,
    recommend_in: NewUserRatings,
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Obter recomendações de um usuário novo.
    """
    recomendations = recommendation_service.create_recommendations(
        recommendation=recommend_in
    )
    return recomendations


@router.get("/{user_id}", response_model=list[Recommendations])
def get_recommendation_by_user_id(
    user: Annotated[User, Depends(valid_user_id)],
    current_user: User = Depends(get_current_user),
):
    """
    Obter recomendacoes do usuário por id.
    """
    return recommendation_service.get_recommendations(user_id=user.id)

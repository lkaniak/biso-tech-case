from typing import Annotated

from api.core.v1.ratings.models import RatingPublic, RatingsCreate, RatingsPublic
from api.core.v1.ratings.schemas import RatingInsert
from fastapi import APIRouter, Depends
from api.core.v1.users.deps import (
    valid_user_id,
    get_current_user,
)
from api.lib.models import User

import api.core.v1.ratings.service as ratings_service

router = APIRouter()


@router.get(
    "/{user_id}",
    response_model=RatingsPublic,
)
def read_ratings_by_user(
    user: Annotated[User, Depends(valid_user_id)],
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> RatingsPublic:
    """
    Obter avaliações do usuário por id.
    """

    list_data = ratings_service.list_ratings(skip=skip, limit=limit, user_id=user.id)

    return RatingsPublic(data=list_data.data, count=list_data.count)


@router.post("/{user_id}/{movie_id}", response_model=RatingPublic)
def create_rating(
    *,
    user_id: int,
    movie_id: int,
    rating_in: RatingInsert,
    current_user: User = Depends(get_current_user),
) -> RatingPublic:
    """
    Criar avaliação
    """
    rating = ratings_service.create_ratings(
        rating_create=rating_in, movie_id=movie_id, user_id=user_id
    )
    return rating

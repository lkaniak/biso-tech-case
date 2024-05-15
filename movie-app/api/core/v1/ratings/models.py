from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel
from sqlmodel import SQLModel


class RatingBase(SQLModel):
    rater_id: int
    movie_rated_id: int
    rating: Decimal
    updated_at: datetime


class RatingPublic(RatingBase):
    id: int


class RatingsCreate(RatingBase):
    rater_id: int
    movie_rated_id: int
    rating: Decimal


class RatingsPublic(BaseModel):
    data: list[RatingBase]
    count: int

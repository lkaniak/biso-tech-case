from typing import Any

from pydantic import BaseModel

from sqlmodel import SQLModel, Field, Relationship


from api.core.v1.ratings.models import RatingBase
from api.core.v1.users.models import UserBase
from api.core.v1.movies.models import MovieBase


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    user_ratings: list["Rating"] = Relationship(back_populates="rater")


class Movie(MovieBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    movie_ratings: list["Rating"] = Relationship(back_populates="movie_rated")


class Rating(RatingBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    rater_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    rater: User | None = Relationship(back_populates="user_ratings")
    movie_rated_id: int | None = Field(
        default=None, foreign_key="movie.id", nullable=False
    )
    movie_rated: Movie | None = Relationship(back_populates="movie_ratings")


class ListData(BaseModel):
    count: int
    data: list[Any]


class Message(SQLModel):
    message: str

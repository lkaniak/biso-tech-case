from api.core.v1.ratings.models import RatingsCreate
from api.core.v1.ratings.schemas import RatingInsert
from api.infrastructure.database.engine import engine
from api.lib.models import ListData, Rating
from sqlmodel import Session, func, select
from datetime import datetime


def list_ratings(user_id, skip=0, limit=100):
    with Session(engine) as session:
        count_statement = (
            select(func.count()).select_from(Rating).where(Rating.rater_id == user_id)
        )
        count = session.exec(count_statement).one()

        statement = select(Rating).offset(skip).limit(limit)
        ratings = session.exec(statement).all()

        return ListData(count=count, data=ratings)


def create_ratings(
    *, rating_create: RatingInsert, user_id: int, movie_id: int
) -> Rating:
    ratings_create = RatingsCreate(
        rater_id=user_id,
        movie_rated_id=movie_id,
        rating=rating_create.rating,
        updated_at=datetime.now(),
    )
    with Session(engine) as session:
        db_obj = Rating.model_validate(
            ratings_create,
        )
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

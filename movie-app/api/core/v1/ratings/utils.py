import random
import numpy as np
from datetime import datetime

from sqlalchemy import insert, Sequence
from sqlmodel import select, Session

from api.lib.models import Movie
from api.lib.models import Rating
from api.lib.models import User
from api.infrastructure.database.engine import engine
from api.infrastructure.database.session import db_session


def generate_rating(users_ids: Sequence[User], movies_ids: Sequence[Movie]):
    chosen_user_id = random.choices(users_ids, k=32)[0]
    chosen_movie_id = random.choices(movies_ids, k=32)[0]
    return Rating(
        rater_id=chosen_user_id,
        movie_rated_id=chosen_movie_id,
        rating=random.choices(
            np.arange(0.0, 5.0, 0.5),
            k=32,
        )[0],
        updated_at=datetime.now(),
    )


def populate_ratings(
    session: Session,
    qty: int,
    max_ratings: int = 1000001,
):
    ratings = session.exec(select(Rating)).all()
    if not len(ratings) > max_ratings:
        movies_ids = session.exec(select(Movie.id)).all()
        users_ids = session.exec(select(User.id)).all()
        generated_ratings = [
            generate_rating(users_ids, movies_ids) for x in range(0, qty + 1)
        ]
        session.execute(insert(Rating), generated_ratings)
        session.commit()


def init_db_ratings() -> None:
    with Session(engine) as session:
        db_session.set(session)

        populate_ratings(session=session, qty=100000)

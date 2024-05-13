import pandas as pd
from sqlalchemy import insert
from sqlmodel import select, Session

from src.core.v1.movies.models import Movie
from src.infrastructure.database.engine import engine
from src.infrastructure.database.session import db_session


def init_db_movies() -> None:
    with Session(engine) as session:
        db_session.set(session)
        movie = session.exec(select(Movie)).first()
        if not movie:
            df = pd.read_csv("./movies.csv")
            df.columns = ["id", "title", "genres"]
            df["id"] = df["id"].astype(int)
            session.execute(insert(Movie), df.to_dict(orient="records"))

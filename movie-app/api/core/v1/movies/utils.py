import os

import pandas as pd
from sqlalchemy import insert
from sqlmodel import select, Session

from api.lib.models import Movie
from api.infrastructure.database.engine import engine
from api.infrastructure.database.session import db_session


def init_db_movies() -> None:
    with Session(engine) as session:
        db_session.set(session)
        movie = session.exec(select(Movie)).first()
        if not movie:
            df = pd.read_csv(os.path.join(os.path.dirname(__file__), "movies.csv"))
            df.columns = ["id", "title", "genres"]
            df["id"] = df["id"].astype(int)
            session.execute(insert(Movie), df.to_dict(orient="records"))
            session.commit()

import os
from typing import Generator

from sqlmodel import Session

from src.infrastructure.database.engine import engine


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def get_url():
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "")
    server = os.getenv("POSTGRES_SERVER", "")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "app")
    return f"postgresql+psycopg://{user}:{password}@{server}:{port}/{db}"

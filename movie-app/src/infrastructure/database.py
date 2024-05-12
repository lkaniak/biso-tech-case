import os
from collections.abc import Generator
from typing import Annotated
from sqlmodel import Session, create_engine, select
from src.infrastructure.settings import settings
from fastapi import Depends

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def get_url():
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "")
    server = os.getenv("POSTGRES_SERVER", "db")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "app")
    return f"postgresql+psycopg://{user}:{password}@{server}:{port}/{db}"


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]

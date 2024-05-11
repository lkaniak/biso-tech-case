from collections.abc import Generator
from typing import Annotated
from sqlmodel import Session, create_engine, select
from src.infrastructure import settings
from fastapi import Depends

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]

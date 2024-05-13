from fastapi import Depends, Request
from sqlmodel import Session

from src.infrastructure.database.session import db_session
from src.infrastructure.database.utils import get_db
from src.main import app


@app.middleware("http")
async def db_session_middleware(
    request: Request, call_next, database_session: Session = Depends(get_db)
):
    token = db_session.set(database_session)
    try:
        response = await call_next(request)
    finally:
        db_session.reset(token)
        await database_session.close()
    return response

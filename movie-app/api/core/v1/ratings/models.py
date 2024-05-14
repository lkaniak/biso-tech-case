from datetime import datetime
from sqlmodel import SQLModel


class RatingBase(SQLModel):
    rating: int
    updated_at: datetime

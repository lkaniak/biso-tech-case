from datetime import datetime
from decimal import Decimal

from sqlmodel import SQLModel


class RatingBase(SQLModel):
    rating: Decimal
    updated_at: datetime

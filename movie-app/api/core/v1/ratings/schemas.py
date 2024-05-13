from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime


class Rating(BaseModel):
    movie_id: int
    user_id: int
    rating: Decimal
    updated_at: datetime

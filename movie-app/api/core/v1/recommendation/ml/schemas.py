from pydantic import BaseModel
from decimal import Decimal


class GenreRatings(BaseModel):
    action = Decimal
    adventure = Decimal
    animation = Decimal
    childrens = Decimal
    comedy = Decimal
    crime = Decimal
    documentary = Decimal
    drama = Decimal
    fantasy = Decimal
    horror = Decimal
    mystery = Decimal
    romance = Decimal
    scifi = Decimal
    thriller = Decimal


class NewUserRatings(BaseModel):
    id: int | None
    ratings: GenreRatings
    rating_avg: Decimal | None
    rating_count: int | None

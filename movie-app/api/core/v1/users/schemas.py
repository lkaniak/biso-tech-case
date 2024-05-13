from pydantic import BaseModel


class Rater(BaseModel):
    id: int
    name: str
    username: str

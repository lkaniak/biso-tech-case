from sqlmodel import Field, SQLModel


class MovieBase(SQLModel):
    genres: str = ""
    title: str = Field(unique=True, index=True)

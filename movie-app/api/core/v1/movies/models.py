from sqlmodel import Field, SQLModel


class MovieBase(SQLModel):
    genres: str = ""
    title: str = Field(unique=True, index=True)


class Movie(MovieBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

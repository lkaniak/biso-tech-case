from sqlmodel import Field, Relationship, SQLModel


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    hashed_password: str = ""
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None
    nickname: str | None = None


class UserCreate(UserBase):
    password: str


class UserRegister(SQLModel):
    email: str
    password: str
    nickname: str
    full_name: str | None = None


class UserUpdate(UserBase):
    email: str | None = None
    nickname: str | None = None
    password: str | None = None
    current_password: str | None = None
    new_password: str | None = None


class UserUpdateMe(SQLModel):
    full_name: str | None = None
    nickname: str | None = None
    email: str | None = None
    current_password: str | None = None
    new_password: str | None = None


class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int

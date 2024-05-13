from sqlmodel import SQLModel


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: dict | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str

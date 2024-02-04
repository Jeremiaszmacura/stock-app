"""Module contains Token pydantic schemas."""
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None  # email
    name: str | None = None
    surname: str | None = None
    is_superuser: bool | None = None

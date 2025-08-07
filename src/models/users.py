from sqlmodel import Field, SQLModel
from pydantic import EmailStr, HttpUrl


class User(SQLModel, table=True):
    id: int = Field(..., primary_key=True)
    email: EmailStr = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    avatar: HttpUrl | None = Field(None)

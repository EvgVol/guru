from pydantic import BaseModel, EmailStr, HttpUrl


class User(BaseModel):
    """Схема пользователя."""

    id: int
    email: EmailStr
    first_name: str
    last_name: str
    avatar: HttpUrl


class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    avatar: str

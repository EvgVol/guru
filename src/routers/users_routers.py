from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Request
from fastapi_pagination import Page, paginate

from src.schemas.users import User

router = APIRouter(prefix="/api/v1/users")


@router.get("/", response_model=Page[User], status_code=HTTPStatus.OK)
def get_users(request: Request) -> Page[User]:
    return paginate(request.app.state.users)


@router.get("/{user_id}", response_model=User, status_code=HTTPStatus.OK)
def get_user(user_id: int, request: Request) -> User:
    users = request.app.state.users
    if user_id > len(users):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    return users[user_id - 1]

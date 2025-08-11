from http import HTTPStatus

from fastapi import APIRouter
from fastapi_pagination import Page, paginate

from src.database import SessionDep
from src.repositories.users_repository import UsersRepository
from src.schemas.users import User, UserCreate

router = APIRouter(prefix="/api/v1/users")


@router.get("/", response_model=Page[User], status_code=HTTPStatus.OK)
def get_users(session: SessionDep = None) -> Page[User]:
    db = UsersRepository(session)
    return paginate(db.get_all())


@router.get("/{user_id}", response_model=User, status_code=HTTPStatus.OK)
def get_user(user_id: int, session: SessionDep = None) -> User:
    db = UsersRepository(session)
    return db.get_by_id(user_id)


@router.post("/", response_model=User, status_code=HTTPStatus.CREATED)
def add_user(data: UserCreate, session: SessionDep = None) -> User:
    db = UsersRepository(session)
    return db.add(data)


@router.delete("/{user_id}", status_code=HTTPStatus.OK)
def delete_user(user_id: int, session: SessionDep) -> None:
    db = UsersRepository(session)
    return db.delete(user_id)


@router.put("/{user_id}", response_model=User, status_code=HTTPStatus.OK)
def put_user(user_id: int, data: UserCreate, session: SessionDep) -> User:
    db = UsersRepository(session)
    return db.put(user_id, data)


@router.patch("/{user_id}", response_model=User, status_code=HTTPStatus.OK)
def patch_user(user_id: int, data: dict, session: SessionDep) -> User:
    db = UsersRepository(session)
    return db.patch(user_id, data)

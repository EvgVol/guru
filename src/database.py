from typing import Annotated

from fastapi import Depends
from decouple import config
from sqlmodel import create_engine, SQLModel, Session, text

engine = create_engine(
    url=config("DATABASE_URL", "sqlite:///database.db"),
    pool_size=config("DATABASE_POOL_SIZE", cast=int, default=10),
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def check_availability() -> bool:
    try:
        with Session(engine) as session:
            session.exec(text("SELECT 1"))
        return True
    except Exception as e:
        print(e)
        return False


SessionDep = Annotated[Session, Depends(get_session)]

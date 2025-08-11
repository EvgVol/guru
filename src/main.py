from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import create_db_and_tables
from src.routers.users_routers import router as users_router
from src.routers.health import router as health_router
from fastapi_pagination import add_pagination


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(health_router, tags=["Health Service"])
app.include_router(users_router, tags=["Users"])

add_pagination(app)

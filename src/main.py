import json
from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.routers.users_routers import router as users_router
from src.schemas.users import User


@asynccontextmanager
async def lifespan(app: FastAPI):
    with open("users.json", "r") as f:
        users_data = json.load(f)
    validated_users = [User.model_validate(user) for user in users_data]
    app.state.users = validated_users
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(users_router, tags=["Users"])

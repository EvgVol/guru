from pydantic import BaseModel


class Service(BaseModel):
    http: str | None = None


class Microservice(BaseModel):
    guru: Service | None = None


class Config(BaseModel):
    app: Microservice | None = None

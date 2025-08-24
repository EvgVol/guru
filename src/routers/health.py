from http import HTTPStatus

from fastapi import APIRouter

from src.database import check_availability
from src.schemas.app import DatabaseStatus


router = APIRouter(prefix="/health")


@router.get("/status", status_code=HTTPStatus.OK)
def database_status() -> DatabaseStatus:
    return DatabaseStatus(status=check_availability())

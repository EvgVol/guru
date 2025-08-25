from app.common.repository import BaseRepository
from app.models.users import User
from sqlmodel import Session


class UsersRepository(BaseRepository[User]):
    """Репозиторий для управления сущностями Users."""

    def __init__(self, session: Session):
        super().__init__(User, session)

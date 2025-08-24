import pytest

from app.schemas.users import UserCreate


@pytest.fixture
def data_new_user(fake) -> UserCreate:
    """
    Генерация данных для создания пользователя.
    """
    return UserCreate(
        email=fake.email(),
        last_name=fake.last_name(),
        first_name=fake.first_name(),
        avatar=fake.image_url(),
    )


@pytest.fixture
def delete_user_by_id(guru_service):
    """
    Фикстура для удаления пользователя по ID после выполнения теста.
    """
    context = {}
    yield context
    url = f"/api/v1/users/{context['user_id']}"
    response = guru_service.delete(url)
    response.raise_for_status()


@pytest.fixture
def create_user(guru_service, data_new_user):
    """
    Фикстура для создания пользователя.
    """
    response = guru_service.post(
        "/api/v1/users/",
        json=data_new_user.model_dump(mode="json"),
    )
    yield response

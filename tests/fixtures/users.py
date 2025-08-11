import pytest
import requests

from src.schemas.users import UserCreate


@pytest.fixture
def data_new_user(fake) -> UserCreate:
    return UserCreate(
        email=fake.email(),
        last_name=fake.last_name(),
        first_name=fake.first_name(),
        avatar=fake.image_url(),
    )


@pytest.fixture
def delete_user_by_id(app_url):
    context = {}
    yield context
    url = f"{app_url}/api/v1/users/{context['user_id']}"
    response = requests.delete(url)
    response.raise_for_status()


@pytest.fixture
def create_user(app_url, data_new_user):
    response = requests.post(
        url=f"{app_url}/api/v1/users/",
        json=data_new_user.model_dump(mode="json"),
    )
    yield response

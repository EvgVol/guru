import pytest
from http import HTTPStatus

import requests


def test_get_users(app_url):
    """Ответ эндпоинта /api/v1/users должен быть 200."""
    url = f"{app_url}/api/v1/users"

    response = requests.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_get_user(app_url, user_id):
    """Ответ эндпоинта /api/v1/user/{user_id} должен быть 200."""
    url = f"{app_url}/api/v1/users/{user_id}"

    response = requests.get(url)
    assert response.status_code == HTTPStatus.OK


def test_get_user_not_found(app_url):
    """
    Ответ эндпоинта /api/v1/user/{user_id} на несуществующего пользоватля должен быть 404."""
    url = f"{app_url}/api/v1/user/100"

    response = requests.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND

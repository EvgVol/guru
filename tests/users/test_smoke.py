from http import HTTPStatus

import requests


def test_get_users(app_url):
    """Ответ эндпоинта /api/v1/users должен быть 200."""
    url = f"{app_url}/api/v1/users"

    response = requests.get(url)
    assert response.status_code == HTTPStatus.OK


def test_response_not_exist(app_url):
    """Ответ эндпоинта /api/v1/users должен быть не пустым."""
    url = f"{app_url}/api/v1/users"

    response = requests.get(url)

    assert len(response.json()) > 0

import pytest
from http import HTTPStatus

import requests

from src.schemas.users import User


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


def test_schema_users(app_url):
    """
    Соответствие схеме User.
    """
    url = f"{app_url}/api/v1/users"

    response = requests.get(url)
    for user in response.json()["items"]:
        User.model_validate(user)


def test_as_list(app_url):
    """
    Ответа в виде списка.
    """
    url = f"{app_url}/api/v1/users"

    response = requests.get(url)
    assert isinstance(response.json()["items"], list)


@pytest.mark.parametrize("size", [1, 10])
def test_count_users_in_response(app_url, size):
    """
    Соответствие количества пользователей в ответе.
    """
    url = f"{app_url}/api/v1/users"
    params = {"size": size}

    response = requests.get(url, params=params)
    assert len(response.json()["items"]) == size


@pytest.mark.parametrize("page", [1, 2])
@pytest.mark.parametrize("size", [5, 10])
def test_pagination(app_url, page, size):
    """
    Проверка пагинации пользователей.
    """
    url = f"{app_url}/api/v1/users?page={page}&size={size}"

    response = requests.get(url).json()
    assert len(response["items"]) <= size


@pytest.mark.parametrize("page1, page2", [(1, 2), (2, 3), (3, 4)])
@pytest.mark.parametrize("size", [5, 1])
def test_different_data_on_different_pages(app_url, page1, page2, size):
    """
    При разных page возвращаются разные данные.
    """
    url = f"{app_url}/api/v1/users"
    params1 = {"page": page1, "size": size}
    params2 = {"page": page2, "size": size}

    response1 = requests.get(url, params=params1).json()["items"]
    response2 = requests.get(url, params=params2).json()["items"]

    ids_page1 = {user["id"] for user in response1}
    ids_page2 = {user["id"] for user in response2}

    assert ids_page1.isdisjoint(ids_page2)

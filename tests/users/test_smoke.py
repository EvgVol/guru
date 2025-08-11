from http import HTTPStatus

import requests


class TestSmoke:
    def test_get_users(self, app_url):
        """
        Ответ эндпоинта /api/v1/users должен быть 200.
        """
        url = f"{app_url}/api/v1/users"

        response = requests.get(url)
        response.raise_for_status()

        assert response.status_code == HTTPStatus.OK

    def test_response_not_exist(self, app_url):
        """
        Ответ эндпоинта /api/v1/users должен быть не пустым.
        """
        url = f"{app_url}/api/v1/users"

        response = requests.get(url)
        response.raise_for_status()

        assert len(response.json()) > 0

    def test_health_database(self, app_url):
        """
        Доступность базы данных.
        """
        url = f"{app_url}/health/status"

        response = requests.get(url)
        response.raise_for_status()

        assert response.json()["status"] is True

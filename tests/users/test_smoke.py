from http import HTTPStatus


class TestSmoke:
    def test_get_users(self, guru_service):
        """
        Ответ эндпоинта /api/v1/users должен быть 200.
        """
        url = "/api/v1/users"

        response = guru_service.get(url)

        assert response.status_code == HTTPStatus.OK

    def test_response_not_exist(self, guru_service):
        """
        Ответ эндпоинта /api/v1/users должен быть не пустым.
        """
        url = "/api/v1/users"

        response = guru_service.get(url)

        assert len(response.json()) > 0

    def test_health_database(self, guru_service):
        """
        Доступность базы данных.
        """
        url = "/health/status"

        response = guru_service.get(url)

        assert response.json()["status"] is True

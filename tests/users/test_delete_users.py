from http import HTTPStatus

import requests


class TestDeleteUsers:
    def test_delete_users(self, app_url, create_user, data_new_user):
        """
        Успешное удаление пользователя.
        """
        user_id = create_user.json()["id"]
        response = requests.delete(url=f"{app_url}/api/v1/users/{user_id}")
        response.raise_for_status()
        assert response.status_code == HTTPStatus.OK

    def test_delete_users_not_found(self, app_url, create_user, data_new_user):
        """
        Удаление несуществующего пользователя.
        """
        user_id = create_user.json()["id"]
        requests.delete(url=f"{app_url}/api/v1/users/{user_id}")
        response = requests.delete(url=f"{app_url}/api/v1/users/{user_id}")
        assert response.status_code == HTTPStatus.NOT_FOUND

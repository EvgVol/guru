from http import HTTPStatus

import requests


class TestUpdateUsers:
    def test_put_user(
        self, app_url, create_user, data_new_user, delete_user_by_id
    ):
        """
        Успешное полное обновление данных пользователя.
        """
        user_id = create_user.json()["id"]
        url = f"{app_url}/api/v1/users/{user_id}"
        data = data_new_user.model_dump(mode="json")

        response = requests.put(url, json=data)
        response.raise_for_status()
        delete_user_by_id.update({"user_id": response.json().get("id")})
        assert response.status_code == HTTPStatus.OK

    def test_patch_user(self, app_url, create_user, delete_user_by_id):
        """
        Успешное частичное обновление данных пользователя.
        """
        user_id = create_user.json()["id"]
        url = f"{app_url}/api/v1/users/{user_id}"
        data = {"last_name": "test"}

        response = requests.patch(url, json=data)
        response.raise_for_status()
        delete_user_by_id.update({"user_id": response.json().get("id")})
        assert response.status_code == HTTPStatus.OK

    def test_patch_user_not_found(self, app_url):
        """
        Попытка обновить несуществующего пользователя.
        """
        user_id = 9999999999999999
        url = f"{app_url}/api/v1/users/{user_id}"
        data = {"last_name": "test"}
        response = requests.patch(url, json=data)
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_fail_update_user(
        self, app_url, create_user, data_new_user, delete_user_by_id
    ):
        """
        Попытка обновить пользователя с некорректными данными.
        """
        delete_user_by_id.update({"user_id": create_user.json().get("id")})
        url = f"{app_url}/api/v1/users/"
        invalid_data = {
            "last_name": data_new_user.last_name,
            "first_name": data_new_user.first_name,
            "avatar": data_new_user.avatar,
        }

        response = requests.post(url, json=invalid_data)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

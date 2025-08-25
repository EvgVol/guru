from http import HTTPStatus


class TestUpdateUsers:
    def test_put_user(
        self, guru_service, create_user, data_new_user, delete_user_by_id
    ):
        """
        Успешное полное обновление данных пользователя.
        """
        user_id = create_user.json()["id"]
        url = f"/api/v1/users/{user_id}"
        data = data_new_user.model_dump(mode="json")

        response = guru_service.put(url, json=data)
        delete_user_by_id.update({"user_id": response.json().get("id")})
        assert response.status_code == HTTPStatus.OK

    def test_patch_user(self, guru_service, create_user, delete_user_by_id):
        """
        Успешное частичное обновление данных пользователя.
        """
        user_id = create_user.json()["id"]
        url = f"/api/v1/users/{user_id}"
        data = {"last_name": "test"}

        response = guru_service.patch(url, json=data)
        response.raise_for_status()
        delete_user_by_id.update({"user_id": response.json().get("id")})
        assert response.status_code == HTTPStatus.OK

    def test_patch_user_not_found(self, guru_service):
        """
        Попытка обновить несуществующего пользователя.
        """
        user_id = 9999999999999999
        url = f"/api/v1/users/{user_id}"
        data = {"last_name": "test"}
        response = guru_service.patch(url, json=data)
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_fail_update_user(
        self, guru_service, create_user, data_new_user, delete_user_by_id
    ):
        """
        Попытка обновить пользователя с некорректными данными.
        """
        delete_user_by_id.update({"user_id": create_user.json().get("id")})
        url = "/api/v1/users/"
        invalid_data = {
            "last_name": data_new_user.last_name,
            "first_name": data_new_user.first_name,
            "avatar": data_new_user.avatar,
        }

        response = guru_service.post(url, json=invalid_data)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

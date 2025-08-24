from http import HTTPStatus


class TestDeleteUsers:
    def test_delete_users(self, guru_service, create_user):
        """
        Успешное удаление пользователя.
        """
        user_id = create_user.json()["id"]
        response = guru_service.delete(f"/api/v1/users/{user_id}")
        response.raise_for_status()
        assert response.status_code == HTTPStatus.OK

    def test_delete_users_not_found(self, guru_service, create_user):
        """
        Удаление несуществующего пользователя.
        """
        user_id = create_user.json()["id"]
        guru_service.delete(f"/api/v1/users/{user_id}")
        response = guru_service.delete(f"/api/v1/users/{user_id}")
        assert response.status_code == HTTPStatus.NOT_FOUND

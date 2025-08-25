import pytest
from http import HTTPStatus

from app.schemas.users import User


class TestGetUsers:
    def test_get_user(
        self, guru_service, create_user, data_new_user, delete_user_by_id
    ):
        """
        Ответ эндпоинта /api/v1/user/{user_id} должен быть 200.
        """
        user_id = create_user.json().get("id")
        delete_user_by_id.update({"user_id": user_id})
        url = f"/api/v1/users/{user_id}"

        response = guru_service.get(url)
        assert response.status_code == HTTPStatus.OK

    def test_get_user_not_found(self, guru_service):
        """
        Ответ эндпоинта /api/v1/user/{user_id} на несуществующего пользоватля должен быть 404.
        """
        url = f"/api/v1/user/{9 * 10**3}"

        response = guru_service.get(url)
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_schema_users(self, guru_service):
        """
        Соответствие схеме User.
        """
        url = "/api/v1/users"

        response = guru_service.get(url)
        for user in response.json()["items"]:
            User.model_validate(user)

    def test_as_list(self, guru_service):
        """
        Ответа в виде списка.
        """
        url = "/api/v1/users"

        response = guru_service.get(url)
        assert isinstance(response.json()["items"], list)

    @pytest.mark.parametrize("size", [1])
    def test_count_users_in_response(
        self, guru_service, size, create_user, delete_user_by_id
    ):
        """
        Соответствие количества пользователей в ответе.
        """
        user_id1 = create_user.json().get("id")
        delete_user_by_id.update({"user_id": user_id1})
        url = "/api/v1/users"
        params = {"size": size}

        response = guru_service.get(url, params=params)
        assert len(response.json()["items"]) == size

    @pytest.mark.parametrize("page", [1, 2])
    @pytest.mark.parametrize("size", [5, 10])
    def test_pagination(self, guru_service, page, size):
        """
        Проверка пагинации пользователей.
        """
        url = f"/api/v1/users?page={page}&size={size}"

        response = guru_service.get(url).json()
        assert len(response["items"]) <= size

    @pytest.mark.parametrize("page1, page2", [(1, 2), (2, 3), (3, 4)])
    @pytest.mark.parametrize("size", [5, 1])
    def test_different_data_on_different_pages(
        self, guru_service, page1, page2, size
    ):
        """
        При разных page возвращаются разные данные.
        """
        url = "/api/v1/users"
        params1 = {"page": page1, "size": size}
        params2 = {"page": page2, "size": size}

        response1 = guru_service.get(url, params=params1).json()["items"]
        response2 = guru_service.get(url, params=params2).json()["items"]

        ids_page1 = {user["id"] for user in response1}
        ids_page2 = {user["id"] for user in response2}

        assert ids_page1.isdisjoint(ids_page2)

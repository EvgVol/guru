from http import HTTPStatus
import pytest

import requests

from src.schemas.users import UserCreate


class TestCreateUser:
    def test_success_create_user(
        self, app_url, data_new_user: UserCreate, delete_user_by_id
    ) -> None:
        """
        Успешное создание пользователя.
        """
        url = f"{app_url}/api/v1/users/"

        response = requests.post(
            url, json=data_new_user.model_dump(mode="json")
        )
        response.raise_for_status()
        delete_user_by_id.update({"user_id": response.json().get("id")})
        assert response.status_code == HTTPStatus.CREATED

    @pytest.mark.parametrize(
        "invalid_payload, expected_status",
        [
            pytest.param(
                lambda valid: {
                    "last_name": valid.last_name,
                    "first_name": valid.first_name,
                    "avatar": valid.avatar,
                },
                HTTPStatus.UNPROCESSABLE_ENTITY,
                id="missing_email",
            ),
            pytest.param(
                lambda valid: {
                    "email": "not-an-email",
                    "last_name": valid.last_name,
                    "first_name": valid.first_name,
                    "avatar": valid.avatar,
                },
                HTTPStatus.UNPROCESSABLE_ENTITY,
                id="invalid_email",
            ),
        ],
    )
    def test_fail_create_user(
        self,
        app_url,
        data_new_user: UserCreate,
        invalid_payload,
        expected_status: HTTPStatus,
    ) -> None:
        """
        Ошибка при создании пользователя.
        """
        url = f"{app_url}/api/v1/users/"
        invalid_data = invalid_payload(data_new_user)

        response = requests.post(url, json=invalid_data)
        assert response.status_code == expected_status

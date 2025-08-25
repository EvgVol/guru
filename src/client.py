import logging
from http import HTTPMethod, HTTPStatus
from typing import Any, Dict, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class Client:
    def __init__(
        self,
        base_url: str,
        timeout: int = 10,
        retries: int = 3,
        backoff: float = 0.3,
        headers: dict[str, str] | None = None,
    ):
        """
        :param base_url: Базовый URL
        :param timeout: Таймаут для запросов (в секундах)
        :param retries: Количество повторных попыток
        :param backoff: Задержка между повторными попытками
        :param headers: Заголовки для запросов
        """
        self.__init_base_params(base_url, timeout)
        self.session = self.__create_session(retries, backoff, headers)
        logging.info(f"Client initialized with base_url={self._base_url}")

    def __init_base_params(self, base_url: str, timeout: int):
        """
        Инициализация базовых параметров
        :param base_url: Базовый URL
        :param timeout: Таймаут для запросов (в секундах)
        """
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    def __create_session(
        self, retries: int, backoff: float, headers: dict[str, str] | None
    ) -> requests.Session:
        """
        Создаем сессию для запросов

        :param retries: Количество повторных попыток
        :param backoff: Задержка между повторными попытками
        :param headers: Заголовки для запросов
        """
        session = requests.Session()
        session.headers.update(self.__init_headers(headers))
        self.__mount_retries(session, retries, backoff)
        return session

    @staticmethod
    def __init_headers(headers: dict[str, str] | None) -> dict:
        """
        Инициализация заголовков по умолчанию
        :param headers: Дополнительные заголовки
        """
        default_headers = {"Content-Type": "application/json"}
        if headers:
            default_headers.update(headers)
        return default_headers

    @staticmethod
    def __mount_retries(
        session: requests.Session, retries: int, backoff: float
    ):
        """
        Реализация повторных попыток
        :param session: Сессия
        :param retries: Количество повторных попыток
        :param backoff: Задержка между повторными попытками
        """
        retry_strategy = Retry(
            total=retries,
            status_forcelist=[
                HTTPStatus.TOO_MANY_REQUESTS,
                HTTPStatus.BAD_GATEWAY,
                HTTPStatus.SERVICE_UNAVAILABLE,
                HTTPStatus.GATEWAY_TIMEOUT,
            ],
            allowed_methods=[
                "HEAD",
                "GET",
                "OPTIONS",
                "POST",
                "PUT",
                "DELETE",
                "PATCH",
            ],
            backoff_factor=backoff,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)

    def _url(self, endpoint: str) -> str:
        """
        Получение полного URL для запроса

        :param endpoint: Путь к API-ресурсу
        """
        return f"{self._base_url}/{endpoint.lstrip('/')}"

    def get(
        self,
        endpoint: str,
        params: Dict[str, Any] | None = None,
        headers: dict[str, Any] = None,
    ) -> requests.Response:
        """
        GET запрос

        :param endpoint: Путь к API-ресурсу
        :param params: Параметры запроса
        :param headers: Заголовки запроса
        """
        return self.send(
            HTTPMethod.GET, endpoint, params=params, headers=headers
        )

    def post(
        self,
        endpoint: str,
        json: Dict[str, Any] | None = None,
        headers: dict[str, Any] = None,
    ) -> requests.Response:
        """
        POST запрос

        :param endpoint: Путь к API-ресурсу
        :param json: JSON тело запроса
        :param headers: Заголовки запроса
        """
        return self.send(HTTPMethod.POST, endpoint, json=json, headers=headers)

    def put(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        headers: dict[str, Any] = None,
    ) -> requests.Response:
        """
        PUT запрос

        :param endpoint: Путь к API-ресурсу
        :param json: JSON тело запроса
        :param headers: Заголовки запроса
        """
        return self.send(HTTPMethod.PUT, endpoint, json=json, headers=headers)

    def patch(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        headers: dict[str, Any] = None,
    ) -> requests.Response:
        """
        PATCH запрос

        :param endpoint: Путь к API-ресурсу
        :param json: JSON тело запроса
        :param headers: Заголовки запроса
        """
        return self.send(
            HTTPMethod.PATCH, endpoint, json=json, headers=headers
        )

    def delete(
        self, endpoint: str, headers: dict[str, Any] = None
    ) -> requests.Response:
        """
        DELETE запрос

        :param endpoint: Путь к API-ресурсу
        :param json: JSON тело запроса
        :param headers: Заголовки запроса
        """
        return self.send(HTTPMethod.DELETE, endpoint, headers=headers)

    def send(
        self, method: HTTPMethod, endpoint: str, **kwargs
    ) -> requests.Response:
        """
        Отправка запроса

        :param method: HTTP метод
        :param endpoint: Путь к API-ресурсу
        :param kwargs: Дополнительные параметры запроса
        """
        url = self._url(endpoint)
        logging.info(f"Request: {method.upper()} {url}, kwargs={kwargs}")
        response = self.session.request(
            method, url, timeout=self._timeout, **kwargs
        )
        logging.info(
            f"Response: status={response.status_code}, body={response.text}"
        )
        return response

    def __enter__(self):
        """
        Контекстный менеджер для создания сессии
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Контекстный менеджер для закрытия сессии
        """
        self.session.close()
        logging.info("Client session closed.")

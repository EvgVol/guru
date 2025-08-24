import pytest

from configs.settings import Settings
from src.client import Client


@pytest.fixture(scope="session")
def guru_service(settings: Settings):
    with Client(settings.config.app.guru.http) as client:
        yield client

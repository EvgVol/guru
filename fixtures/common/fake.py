import pytest
from faker import Faker


@pytest.fixture(scope="session")
def fake() -> Faker:
    """Общая фикстура для генерации тестовых данных."""
    return Faker()

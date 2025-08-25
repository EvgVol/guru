from configs.settings import Settings
import pytest


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings()

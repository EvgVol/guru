import os

import pytest
from dotenv import load_dotenv


@pytest.fixture(autouse=True)
def env():
    load_dotenv()


@pytest.fixture
def app_url():
    return os.getenv("APP_URL")

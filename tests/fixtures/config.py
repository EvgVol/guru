import pytest
from dotenv import load_dotenv
from decouple import config
from faker import Faker


@pytest.fixture(autouse=True)
def env():
    load_dotenv()


@pytest.fixture
def app_url():
    return config("APP_URL", "127.0.0.1:8000")


@pytest.fixture
def fake():
    fake = Faker()
    return fake

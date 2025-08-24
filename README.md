# FastAPI Microservice + API Autotests

## Описание проекта
Этот проект включает в себя:
* Микросервис на Python с использованием FastAPI
* Тесты API

##  Стек технологий

- Python 3.12+
- FastAPI
- Uvicorn
- Pytest
- Allure
- Requests
- Pydantic
- SQLModel
- Sqlalchemy

## Как запустить микросервис
### Локально:
    `poetry run fastapi dev src/main.py`
### Через Dockerfile:
     docker build -t fast_app .
     docker run \
     -p 8000:80 \
     -e APP_URL=http://127.0.0.1:8000 \
     -e DATABASE_URL=postgresql+psycopg2://postgres:example@host.docker.internal:5432/postgres \
     -e DATABASE_POOL_SIZE=10 \
      app

* Примечание: Предварительно БД к которой мы подключаемся должно быть запущена предварительно

### Через Dockerfile:
     `docker compose up --build`




## Как запустить тесты

`poetry run pytest`

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
- Pydantic-Settings
- SQLModel
- Sqlalchemy
- Faker

## Как запустить микросервис

### Локально:
    `poetry run fastapi dev app/main.py`
### Через Docker:
     `docker compose up --build`




## Как запустить тесты

`poetry run pytest`

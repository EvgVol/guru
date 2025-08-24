from http import HTTPStatus
from typing import Generic, TypeVar, Type

from fastapi import HTTPException
from pydantic import BaseModel
from sqlmodel import SQLModel, select, delete, Session


T = TypeVar("T", bound=SQLModel)
S = TypeVar("S", bound=BaseModel)


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.session = session

    def get_by_id(self, obj_id: int) -> T | None:
        """Получить объект модели по ID."""
        query = select(self.model).where(self.model.id == obj_id)
        result = self.session.exec(query)
        item = result.first()
        if not item:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Apologize, not found!",
            )
        return item

    def get_all(self):
        """Получить все объекты модели из базы данных."""
        result = self.session.exec(select(self.model))
        return result.all()

    def add(self, obj: S) -> T:
        """Добавить объект в базу данных."""
        request_data = self.model(**obj.model_dump())
        self.session.add(request_data)
        try:
            self.session.commit()
            self.session.refresh(request_data)
            return request_data
        except Exception as e:
            self.session.rollback()
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail=str(e)
            )

    def delete(self, obj_id: int) -> None:
        """Удалить объект модели по ID."""
        instance = self.get_by_id(obj_id)
        if not instance:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"{self.model.__name__} not found",
            )

        self.session.delete(instance)
        self.session.commit()
        return {"message": "Объект успешно удален"}

    def clear(self) -> None:
        """Удалить все объекты модели из базы данных."""
        self.session.exec(delete(self.model))
        self.session.commit()
        return {"message": "Объекты успешно удалены"}

    def put(self, obj_id: int, obj: S) -> T:
        """Полностью обновить объект в базе данных."""
        instance = self.get_by_id(obj_id)
        if not instance:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Item not found"
            )

        update_data = obj.model_dump()
        for key, value in update_data.items():
            setattr(instance, key, value)

        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    def patch(self, obj_id: int, data: dict) -> T:
        """Частично обновить поля объекта по его ID."""
        instance = self.get_by_id(obj_id)
        if not instance:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Item not found"
            )

        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance

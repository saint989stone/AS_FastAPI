"""
Паттерн DataMapper позволяет связать модель и схему без их взаимозависиомости.
То есть модель не привязана к схеме, а схема к модели.

"""
from typing import TypeVar
from pydantic import BaseModel
from src.database import Base

DBModelType = TypeVar('DBModelType', bound=Base)
SchemaType = TypeVar('SchemaType', bound=BaseModel)

class DataMapper:
    db_model: type[DBModelType] = None
    schema: type[SchemaType] = None

    @classmethod
    def map_to_domain_entity(cls, data):
        """
        Функция превращает модель SQLAlchemy в pydantic схему
        """
        return cls.schema.model_validate(data, from_attributes=True)
    @classmethod
    def map_to_persistent_entity(cls, data):
        """
        Функция превращает pydantic схему в модель SQLAlchemy
        """
        return cls.db_model(**data.model_dump())
from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel

ModelType = TypeVar('ModelType')
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class BaseService(ABC, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: ModelType) -> None:
        self.model: ModelType = model

    @abstractmethod
    def get_one(self, id: int) -> Optional[ModelType]:
        pass

    @abstractmethod
    def get_many(
        self, *, offset: int = 0, limit: int = 100
    ) -> List[ModelType]:
        pass

    @abstractmethod
    def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        pass

    @abstractmethod
    def update(
        self, *, obj_id: str, obj_in: UpdateSchemaType
    ) -> ModelType:
        pass

    @abstractmethod
    def remove(self, *, id: int) -> ModelType:
        pass

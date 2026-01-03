from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session

ModelType = TypeVar('ModelType')
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class BaseService(ABC, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: ModelType, session: None | Session) -> None:
        self.model: ModelType = model
        self.session = session

    @abstractmethod
    def get_one(self, id: int) -> Optional[ModelType]:
        pass  # pragma: no cover

    @abstractmethod
    def get_many(
        self, *, offset: int = 0, limit: int = 100
    ) -> List[ModelType]:
        pass  # pragma: no cover

    @abstractmethod
    def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        pass  # pragma: no cover

    @abstractmethod
    def update(self, *, obj_id: str, obj_in: UpdateSchemaType) -> ModelType:
        pass  # pragma: no cover

    @abstractmethod
    def remove(self, *, id: int) -> ModelType:
        pass  # pragma: no cover

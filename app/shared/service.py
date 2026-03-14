from abc import ABC
from typing import Generic, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.crud import CRUDBase

ModelType = TypeVar('ModelType')
CreateSchemaType = TypeVar('CreateSchemaType')
UpdateSchemaType = TypeVar('UpdateSchemaType')


class BaseService(ABC, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession) -> None:
        self.session = session
        self.repo = CRUDBase[ModelType, CreateSchemaType, UpdateSchemaType](
            model, session
        )

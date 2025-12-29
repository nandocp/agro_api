# from abc import ABC, abstractmethod
# from typing import Generic, List, Optional, TypeVar

# from pydantic import BaseModel
# from sqlalchemy.orm import Session

# ModelType = TypeVar('ModelType')
# CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
# UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


# class ServiceBase(
# ABC, Generic[ModelType, CreateSchemaType, UpdateSchemaType]
# ):
#     def __init__(self, model: ModelType):
#         self.model = model

#     @abstractmethod
#     def get_one(self, db: Session, id: int) -> Optional[ModelType]:
#         pass

#     @abstractmethod
#     def get_many(
#         self, db: Session, *, skip: int = 0, limit: int = 100
#     ) -> List[ModelType]:
#         pass

#     @abstractmethod
#     def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
#         pass

#     @abstractmethod
#     def update(
#         self, db: Session, *, db_obj: ModelType, obj_in: UpdateSchemaType
#     ) -> ModelType:
#         pass

#     @abstractmethod
#     def remove(self, db: Session, *, id: int) -> ModelType:
#         pass

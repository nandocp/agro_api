from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

ModelType = TypeVar('ModelType', bound=Any)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)
UpdateType = Union[UpdateSchemaType, Dict[str, Any]]


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], session: Session = None):
        self.session: Session | None = session
        self.model = model

    async def get_by(self, params: dict) -> Optional[ModelType]:
        stmt = select(self.model)

        for col, val in params.items():
            stmt = stmt.where(getattr(self.model, col) == val)

        return await self.session.scalar(stmt)

    async def get_one(self, id: str) -> Optional[ModelType]:
        return await self.session.scalar(
            select(self.model).filter(self.model.id == id)
        )

    async def get_many(
        self, filters, *, offset: int = 0, limit: int = 100
    ) -> List[ModelType]:
        stmt = select(self.model).offset(offset).limit(limit)

        for column, value in filters.items():
            stmt = stmt.filter(getattr(self.model, column) == value)

        objs_list = await self.session.scalars(stmt)
        return objs_list.all()

    async def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def update(
        self, *, db_obj: ModelType, obj_in: UpdateType,
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def remove(self, *, id: int) -> ModelType:
        obj = self.session.query(self.model).get(id)
        self.session.delete(obj)
        await self.session.commit()
        return obj

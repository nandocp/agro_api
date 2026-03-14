from typing import Any, Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar('ModelType')
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_one(self, id: Any) -> ModelType | None:
        return await self.session.get(self.model, id)

    async def get_by(self, params: dict[str, Any]) -> ModelType | None:
        stmt = select(self.model)
        for col, val in params.items():
            stmt = stmt.where(getattr(self.model, col) == val)
        return await self.session.scalar(stmt)

    async def get_many(
        self,
        filters: dict[str, Any] | None = None,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> list[ModelType]:
        stmt = select(self.model).offset(offset).limit(limit)
        for col, val in (filters or {}).items():
            stmt = stmt.where(getattr(self.model, col) == val)
        result = await self.session.scalars(stmt)
        return result.all()

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.model_dump())
        self.session.add(db_obj)
        await self.session.flush()
        return db_obj

    async def update(
        self,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any],
    ) -> ModelType:
        update_data = (
            obj_in
            if isinstance(obj_in, dict)
            else obj_in.model_dump(exclude_unset=True)
        )
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        self.session.add(db_obj)
        await self.session.flush()
        return db_obj

    async def delete(self, db_obj: ModelType) -> None:
        await self.session.delete(db_obj)
        await self.session.flush()

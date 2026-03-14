"""
At the Repo level, we only flush data changed, creating rollbackable changes.
Commiting permanently happens at router level.
"""

from typing import Any, Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar('ModelType')
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel, default=Any)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel, default=Any)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    def _apply_filters(self, stmt: Select, filters: dict[str, Any]) -> Select:
        for col, val in filters.items():
            column = getattr(self.model, col)
            stmt = stmt.where(
                column.is_(None) if val is None else column == val
            )
        return stmt

    async def get_one(self, id: Any) -> ModelType | None:
        return await self.session.get(self.model, id)

    async def get_by(self, params: dict[str, Any]) -> ModelType | None:
        stmt = self._apply_filters(select(self.model), params)
        return await self.session.scalar(stmt)

    async def get_many(
        self,
        filters: dict[str, Any] | None = None,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> list[ModelType]:
        stmt = self._apply_filters(
            select(self.model).offset(offset).limit(limit), (filters or {})
        )
        result = await self.session.scalars(stmt)
        return result.all()

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.model_dump())
        return await self.save(db_obj)

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

        return await self.save(db_obj)

    async def save(self, db_obj: ModelType) -> ModelType:
        self.session.add(db_obj)
        # Adicionar logger para, quando em desenvolvimento,
        # verificar se o objeto está sendo adicionado corretamente
        # utilizar self.session.new
        await self.session.flush()
        # Pode colocar um logger aqui para, quando em desenolvimento,
        # inspecionar o objeto que foi flushed.
        # utilizar self.session.identity_map.values()
        return db_obj

    async def delete(self, db_obj: ModelType) -> None:
        await self.session.delete(db_obj)
        await self.session.flush()

"""
At the Repo level, we only flush data changed, creating rollbackable changes.
Commiting permanently happens at router level.
"""

from typing import Any, Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.schemas import PaginatedResponse
from config.logging import logger

ModelType = TypeVar('ModelType')
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel, default=Any)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel, default=Any)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    """
    Override in specific repositories to customize filter behavior.
    Default: exact match.
    """

    def _build_filter_clause(self, col: str, val: Any):
        column = getattr(self.model, col)
        if val is None:
            return column.is_(None)
        return column == val

    def _apply_filters(self, stmt: Select, filters: dict[str, Any]) -> Select:
        for col, val in filters.items():
            stmt = stmt.where(self._build_filter_clause(col, val))

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
    ) -> PaginatedResponse:
        stmt = select(self.model).offset(offset).limit(limit)

        if filters:
            stmt = self._apply_filters(stmt, filters)
        result = await self.session.scalars(stmt)
        data = result.all()

        count_stmt = select(func.count()).select_from(self.model)
        if filters:
            count_stmt = self._apply_filters(count_stmt, filters)
        total = await self.session.scalar(count_stmt) or 0

        return PaginatedResponse(
            data=data,
            total=total,
            offset=offset,
            limit=limit,
            has_next=offset + limit < total,
            has_previous=offset > 0,
        )

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

        logger.debug(
            'Adding object to session',
            extra={
                'model': db_obj.__class__.__name__,
                'pending': [
                    obj.__class__.__name__ for obj in self.session.new
                ],
            },
        )

        await self.session.flush()
        await self.session.refresh(db_obj)

        logger.debug(
            'Object flushed and refreshed',
            extra={
                'model': db_obj.__class__.__name__,
                'identity_map': [
                    f'{obj.__class__.__name__}({obj.id})'
                    for obj in self.session.identity_map.values()
                    if hasattr(obj, 'id')
                ],
            },
        )

        return db_obj

    async def delete(self, db_obj: ModelType) -> None:
        await self.session.delete(db_obj)
        await self.session.flush()

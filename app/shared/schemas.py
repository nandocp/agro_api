from datetime import datetime
from typing import Generic, TypeVar

from pydantic import UUID7, BaseModel, Field

from config.settings import settings

T = TypeVar('T')


class Pagination(BaseModel):
    offset: int | None = Field(ge=0, default=0)
    limit: int | None = Field(ge=0, default=settings.PAGINATION_LIMIT)


class PaginatedResponse(BaseModel, Generic[T]):
    data: list[T]
    total: int
    offset: int
    limit: int
    has_next: bool
    has_previous: bool


class BaseSchema(BaseModel):
    id: UUID7
    created_at: datetime
    updated_at: datetime

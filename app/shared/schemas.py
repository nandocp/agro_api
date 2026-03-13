from datetime import datetime

from pydantic import UUID7, BaseModel, Field


class Pagination(BaseModel):
    offset: int | None = Field(ge=0, default=0)
    limit: int | None = Field(ge=0, default=10)


class BaseSchema(BaseModel):
    id: UUID7
    created_at: datetime
    updated_at: datetime

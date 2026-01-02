from datetime import datetime

from pydantic import UUID4, BaseModel, Field


class FilterPage(BaseModel):
    offset: int = Field(ge=0, default=0)
    limit: int = Field(ge=0, default=10)


class BaseSchema(BaseModel):
    id: UUID4
    created_at: datetime
    updated_at: datetime

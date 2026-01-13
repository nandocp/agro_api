from datetime import datetime

from pydantic import UUID4, BaseModel, ConfigDict, Field

from agro_api.entities.estate import EstateKind
from agro_api.schemas.common import Pagination


class EstateBase(BaseModel):
    label: str
    slug: str
    description: str | None
    kind: EstateKind
    opened_at: datetime | None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        from_attrbutes=True,
    )


class EstateCreate(EstateBase):
    user_id: UUID4 | None


class EstateItem(EstateBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime


class EstatesList(BaseModel):
    estates: list[EstateItem]


class EstateFilter(Pagination):
    label: str | None = Field(default=None, min_length=3, max_length=32)
    slug: str | None = Field(default=None, min_length=3)
    kind: EstateKind | None = Field(default=None)
    opened_at: datetime | None = Field(default=None)

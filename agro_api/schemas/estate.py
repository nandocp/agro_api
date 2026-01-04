from datetime import datetime

from pydantic import UUID4, BaseModel, ConfigDict, Field

from agro_api.entities.estate import EstateKind
from agro_api.schemas.common import FilterPage


class EstateBase(BaseModel):
    label: str
    slug: str
    kind: EstateKind
    model_config = ConfigDict(from_attrbutes=True)


class EstateCreate(EstateBase):
    opened_at: datetime


class EstateItem(EstateCreate):
    id: UUID4
    user_id: UUID4
    created_at: datetime
    updated_at: datetime
    closed_at: datetime


class EstatesList(BaseModel):
    estates: list[EstateItem]


class EstateUpdate(EstateCreate):
    closed_at: datetime | None


class EstateFilter(FilterPage):
    label: str | None = Field(default=None, min_length=3, max_length=32)
    slug: str | None = Field(default=None, min_length=3)
    kind: EstateKind | None = None

from datetime import datetime

from pydantic import UUID4, BaseModel, ConfigDict, Field

from agro_api.entities.estate import EstateKind
from agro_api.schemas.common import FilterPage


class EstateBase(BaseModel):
    label: str
    slug: str
    kind: EstateKind
    model_config = ConfigDict(from_attrbutes=True)


class EstatePostPayloadSchema(EstateBase):
    opened_at: datetime


class EstatePostResponseSchema(EstatePostPayloadSchema):
    id: UUID4
    created_at: datetime
    updated_at: datetime


class EstateGetResponseSchema(EstatePostResponseSchema):
    closed_at: datetime | None
    user_id: UUID4


class EstateFilter(FilterPage):
    label: str | None = Field(default=None, min_length=3, max_length=32)
    slug: str | None = Field(default=None, min_length=3)
    kind: EstateKind | None = None


class EstatesList(BaseModel):
    estates: list[EstateGetResponseSchema]

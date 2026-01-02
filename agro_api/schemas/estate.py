from datetime import datetime

from pydantic import UUID4, BaseModel, ConfigDict

from agro_api.entities.estate import EstateKind


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

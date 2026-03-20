# app/domain/estates/schemas/estate.py
from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID
from zoneinfo import available_timezones

from pydantic import BaseModel, Field, field_validator, model_validator

from app.domain.estates.enums import (
    EstateUsage,
    EstateZone,
    OwnershipType,
)
from app.shared.enums import GeometrySource
from app.shared.geometry import (
    validate_multipolygon_wkt,
    validate_point_within_boundary,
    validate_point_wkt,
)
from app.shared.utils import slugify

_VALID_TIMEZONES = available_timezones()


class EstateCreate(BaseModel):
    label: str = Field(min_length=1, max_length=96)
    slug: str | None = Field(None, min_length=5, max_length=64)
    description: str | None = Field(None, max_length=200)
    timezone: str = Field(default='America/Sao_Paulo', max_length=64)
    zone: EstateZone = Field(default=EstateZone.RURAL)
    usage: EstateUsage | None = Field(None)
    ownership_type: OwnershipType = Field(default=OwnershipType.OWNED)

    opened_at: date | None = Field(None)
    declared_area_m2: Decimal | None = Field(None, gt=0)

    boundary_wkt: str | None = Field(None)
    entrance_point_wkt: str | None = Field(None)
    boundary_source: GeometrySource | None = Field(None)

    @field_validator('boundary_wkt')
    @classmethod
    def check_boundary(cls, v: str | None) -> str | None:
        if v is None:
            return None

        return validate_multipolygon_wkt(v)

    @field_validator('entrance_point_wkt')
    @classmethod
    def check_entrance_point(cls, v: str | None) -> str | None:
        if v is None:
            return v
        return validate_point_wkt(v)

    @field_validator('timezone')
    @classmethod
    def validate_timezone(cls, v: str) -> str:
        if v not in _VALID_TIMEZONES:
            raise ValueError(f'Invalid timezone: {v}')
        return v

    @model_validator(mode='after')
    def check_point_within_boundary(self) -> 'EstateCreate':
        if self.entrance_point_wkt and self.boundary_wkt:
            validate_point_within_boundary(
                self.entrance_point_wkt,
                self.boundary_wkt,
            )
        return self

    @model_validator(mode='after')
    def generate_slug_from_label(self) -> 'EstateCreate':
        if not self.slug:
            self.slug = slugify(self.label)
        return self


class EstateResponse(BaseModel):
    """Schema para resposta do Estate."""

    id: UUID
    account_id: UUID
    label: str

    model_config = {'from_attributes': True}

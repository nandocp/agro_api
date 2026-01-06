from datetime import datetime
from typing import Any, List

from pydantic import UUID4, BaseModel, ConfigDict, Field, validator

from agro_api.entities.estate import EstateKind
from agro_api.schemas.common import FilterPage
from config.geometry import dump_geometry


class EstateBase(BaseModel):
    label: str
    slug: str
    kind: EstateKind
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        from_attrbutes=True,
    )


class EstateCreate(EstateBase):
    opened_at: datetime


class EstateItem(EstateCreate):
    id: UUID4
    user_id: UUID4
    coordinates: Any
    limits: Any
    created_at: datetime
    updated_at: datetime
    closed_at: datetime | None
    divisions: List[Any]

    _validate_limit = validator(
        'limits', pre=True, allow_reuse=True
    )(dump_geometry)

    _validate_coordinates = validator(
        'coordinates', pre=True, allow_reuse=True
    )(dump_geometry)


class EstatesList(BaseModel):
    estates: list[EstateItem]


class EstateUpdate(EstateCreate):
    closed_at: datetime | None
    coordinates: Any  # Optional[Tuple[float, float]] = None
    limits: Any  # Optional[List[Tuple[float, float]]] = None

    # _validate_limit = validator(
    #     'limits', pre=True, always=True, allow_reuse=True
    # )(create_polygon_geometry)

    # _validate_coordinates = validator(
    #     'coordinates', pre=True, always=True, allow_reuse=True
    # )(create_point_geometry)


class EstateFilter(FilterPage):
    label: str | None = Field(default=None, min_length=3, max_length=32)
    slug: str | None = Field(default=None, min_length=3)
    kind: EstateKind | None = None

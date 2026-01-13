from typing import Any, Optional

from pydantic import UUID4, BaseModel, ConfigDict, validator

from agro_api.entities.estate.plot import LandUses, PlotStatus
from config.geometry import dump_geometry


class EstatePlotBase(BaseModel):
    label: str | None
    slug: str | None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        from_attrbutes=True,
    )


class EstatePlotCreate(EstatePlotBase):
    estate_id: UUID4
    land_use: LandUses
    status: Optional[PlotStatus]
    limits: Optional[Any]

    _validate_limits = validator('limits', pre=True, allow_reuse=True)(
        dump_geometry
    )


class PlotItem(EstatePlotCreate):
    id: UUID4
    origin_plot_id: Optional[UUID4] | None


class EstatePlotUpdate(EstatePlotBase):
    land_use: LandUses
    note: Optional[str]
    status: Optional[PlotStatus]
    limits: Optional[Any]


# class EstateItem(EstateCreate):
#     id: UUID4
#     user_id: UUID4
#     coordinates: Any
#     limits: Any
#     created_at: datetime
#     updated_at: datetime
#     closed_at: Optional[datetime]
#     plots: List[Any]

#     _validate_limit = validator(
#         'limits', pre=True, allow_reuse=True
#     )(dump_geometry)

#     _validate_coordinates = validator(
#         'coordinates', pre=True, allow_reuse=True
#     )(dump_geometry)


# class EstatesList(BaseModel):
#     estates: list[EstateItem]


# class EstateUpdate(EstateCreate):
#     closed_at: datetime | None
#     coordinates: Any  # Optional[Tuple[float, float]] = None
#     limits: Any  # Optional[List[Tuple[float, float]]] = None

#     # _validate_limit = validator(
#     #     'limits', pre=True, always=True, allow_reuse=True
#     # )(create_polygon_geometry)

#     # _validate_coordinates = validator(
#     #     'coordinates', pre=True, always=True, allow_reuse=True
#     # )(create_point_geometry)


# class EstateFilter(FilterPage):
#     label: str | None = Field(default=None, min_length=3, max_length=32)
#     slug: str | None = Field(default=None, min_length=3)
#     kind: EstateKind | None = None

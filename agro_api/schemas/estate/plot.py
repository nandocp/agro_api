from typing import Optional

from pydantic import UUID4, BaseModel, ConfigDict, Field

from agro_api.entities.estate.plot import LandUses, PlotStatus
from agro_api.schemas.common import Pagination


class PlotBase(BaseModel):
    label: str | None
    slug: str | None
    land_use: LandUses
    status: Optional[PlotStatus]
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        from_attrbutes=True,
    )


class PlotCreate(PlotBase):
    estate_id: UUID4
    created_by: UUID4 | None


class PlotItem(PlotCreate):
    id: UUID4


class PlotUpdate(PlotBase):
    note: Optional[str]


class PlotFilter(Pagination):
    slug: str | None = Field(default=None, min_length=3)
    land_use: LandUses | None = Field(default=None)
    status: PlotStatus | None = Field(default=None)


class PlotsList(BaseModel):
    plots: list[PlotItem]

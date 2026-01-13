from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, UniqueConstraint, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
)

from agro_api.entities.base import table_registry
from config.geometry import area_from_wkb


class LandUses(str, Enum):
    agriculture = 'agriculture'
    pasture = 'pasture'
    industry = 'industry'
    leisure = 'leisure'
    water = 'water'
    infrastructure = 'infrastructure'
    preservation = 'preservation'


class PlotStatus(str, Enum):
    active = 'active'
    inactive = 'inactive'
    merged = 'merged'
    divided = 'divided'


@mapped_as_dataclass(table_registry)
class Plot:
    __tablename__ = 'estate_plots'
    __table_args__ = (UniqueConstraint('estate_id', 'slug'),)

    id: Mapped[Uuid] = mapped_column(
        UUID,
        init=False,
        primary_key=True,
        server_default=func.gen_random_uuid(),
        nullable=False,
    )

    estate_id: Mapped[Uuid] = mapped_column(ForeignKey('estates.id'))
    origin_plot_id: Mapped[Uuid] = mapped_column(
        ForeignKey('estate_plots.id'), nullable=True, init=False
    )

    land_use: Mapped[LandUses] = mapped_column(nullable=False)

    slug: Mapped[str] = mapped_column(nullable=False)

    label: Mapped[str] = mapped_column(unique=False)

    status: Mapped[PlotStatus] = mapped_column(default=PlotStatus('active'))

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    estate = relationship('Estate', back_populates='plots', lazy='selectin')

    def area(self):
        return area_from_wkb(self.limits, formatter=2)

from __future__ import annotations

from datetime import datetime
from enum import Enum

from geoalchemy2 import Geometry
from sqlalchemy import ForeignKey, UniqueConstraint, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
)

from agro_api.entities.base import table_registry
from config.geometry import wkb_to_shape


class LandUses(Enum):
    agriculture = 'agriculture'
    pasture = 'pasture'
    industry = 'industry'
    leisure = 'leisure'
    water = 'water'
    infrastructure = 'infrastructure'
    preservation = 'preservation'


class PlotStatus(Enum):
    active = "active"
    inactive = "inactive"
    merged = "merged"
    divided = "divided"


@mapped_as_dataclass(table_registry)
class EstatePlot:
    __tablename__ = 'estate_plots'
    __table_args__ = (
        UniqueConstraint('estate_id', 'slug'),
    )

    id: Mapped[Uuid] = mapped_column(
        UUID,
        init=False,
        primary_key=True,
        server_default=func.gen_random_uuid(),
        nullable=False,
    )

    estate_id: Mapped[Uuid] = mapped_column(ForeignKey('estates.id'))
    origin_plot_id: Mapped[Uuid] = mapped_column(
        ForeignKey('estate_plots.id'),
        nullable=True,
        init=False
    )

    land_use: Mapped[LandUses] = mapped_column(nullable=False)

    note: Mapped[str] = mapped_column(default='')

    status: Mapped[PlotStatus] = mapped_column(
        default=PlotStatus('active')
    )

    limits: Mapped[Geometry] = mapped_column(
        Geometry(geometry_type='POLYGON', srid=4326),
        nullable=True,
        init=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    slug: Mapped[str] = mapped_column(nullable=False, default='')

    label: Mapped[str] = mapped_column(unique=False, default='')

    estate = relationship(
        'Estate', init=False, back_populates='plots'
    )

    def area(self):
        if not self.limits:
            return None

        shape = wkb_to_shape(self.limits)
        return f'{shape.area:.2f}'

    def __repr__(self):
        attrs = [
            f'estate={self.estate.slug}',
            f'slug={self.slug}',
            f'area={self.area()}'
        ]
        return f'<EstatePlot({', '.join(attrs)})>'

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from geoalchemy2 import Geometry
from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    Uuid,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
)

from agro_api.entities.base import BaseEntity
from config.database import table_registry

if TYPE_CHECKING:
    from agro_api.entities.plot import Plot
    from agro_api.entities.activity import Planting


@mapped_as_dataclass(table_registry, kw_only=True)
class Zone(BaseEntity):
    """A management unit within a plot – the actual location where plantings happen."""
    __tablename__ = 'zones'

    # Required foreign key to plot
    plot_id: Mapped[Uuid] = mapped_column(
        ForeignKey('plots.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )

    # Human‑readable identification
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(200))

    # Area – always known (even without geometry)
    area_ha: Mapped[Decimal] = mapped_column(
        Numeric(10, 4),
        nullable=False,
        comment="Area in hectares, always provided by the user"
    )

    # Geometry (optional) – for farmers who have GPS/mapping
    boundary: Mapped[Geometry | None] = mapped_column(
        Geometry(geometry_type='POLYGON', srid=4326, spatial_index=True),
        nullable=True,
        comment="Geometric boundary of the zone (if available)"
    )

    # Fallback location description (for zones without geometry)
    reference_location: Mapped[str | None] = mapped_column(
        String(200),
        comment="e.g., 'Behind the barn', 'Along the creek' – used when geometry not available"
    )

    # Physical characteristics (optional overrides of plot defaults)
    soil_type_id: Mapped[Uuid | None] = mapped_column(
        ForeignKey('soil_types.id', ondelete='SET NULL'),
        comment="Soil type if different from the plot's predominant soil"
    )
    drainage_class: Mapped[str | None] = mapped_column(String(50))
    slope_class: Mapped[str | None] = mapped_column(String(50))

    # Temporal validity (zones can be split, merged, or retired)
    active_from: Mapped[date] = mapped_column(
        server_default=func.current_date(),
        nullable=False
    )
    active_to: Mapped[date | None] = mapped_column(
        comment="NULL means currently active"
    )

    # Relationships
    plot: Mapped['Plot'] = relationship(back_populates='zones')
    plantings: Mapped[List['Planting']] = relationship(
        back_populates='zone',
        cascade='all, delete-orphan',
        init=False
    )

    __table_args__ = (
        # Ensure names are unique within a plot at any given time
        Index('ix_zone_plot_name_active', 'plot_id', 'name', 'active_from'),
        CheckConstraint(
            'area_ha > 0',
            name='ck_zone_area_positive'
        ),
    )

    def __repr__(self):
        return f"Zone(id={self.id}, name={self.name}, plot={self.plot_id})"

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING, List

from geoalchemy2 import Geometry
from sqlalchemy import (
    Computed,
    ForeignKey,
    Numeric,
    String,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
)

from config.database import table_registry
from config.geometry import GeometrySource

if TYPE_CHECKING:
    from agro_api.entities.core import User
    from agro_api.entities.estate import Estate
    from agro_api.entities.plot import PlotProtection  # , PlotTransition


class PlotStatus(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    TRANSITIONED = 'transitioned'


@mapped_as_dataclass(table_registry)
class Plot:
    __tablename__ = 'plots'
    __table_args__ = (
        UniqueConstraint('estate_id', 'slug', name='idx_plot_estate_slug'),
    )

    id: Mapped[Uuid] = mapped_column(
        UUID,
        init=False,
        primary_key=True,
        server_default=func.uuidv7(),
        nullable=False,
    )

    estate_id: Mapped[Uuid] = mapped_column(
        ForeignKey('estates.id', ondelete='CASCADE')
    )
    creator_id: Mapped[Uuid] = mapped_column(
        ForeignKey('users.id', ondelete='RESTRICT')
    )

    slug: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True,
        comment='URL-safe identifier within Estate'
    )

    label: Mapped[str] = mapped_column(
        String(96), comment='Human-readable name'
    )

    boundary: Mapped[Geometry] = mapped_column(
        Geometry(
            geometry_type='POLYGON',
            spatial_index=True,
            srid=4326,
        ),
        nullable=False,  # Plot must have a boundary
        comment="Plot boundary polygon"
    )
    boundary_source: Mapped[GeometrySource | None]

    # Computed measurements (same pattern as Estate)
    calculated_area_m2: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),  # Slightly smaller than estate (plots are smaller)
        Computed(
            """
            CASE
                WHEN boundary IS NOT NULL
                THEN ST_Area(boundary::geography)
                ELSE NULL
            END
            """,
            persisted=True
        ),
        nullable=True
    )

    perimeter_m: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        Computed(
            """
            CASE
                WHEN boundary IS NOT NULL
                THEN ST_Perimeter(boundary::geography)
                ELSE NULL
            END
            """,
            persisted=True
        ),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    creator: Mapped['User'] = relationship()
    estate: Mapped['Estate'] = relationship(
        back_populates='plots', lazy='joined'
    )

    # # Transitions where this plot is the predecessor (it was replaced)
    # transitions_as_predecessor:
    # Mapped[List['PlotTransition']] = relationship(
    #     foreign_keys='PlotTransition.predecessor_id',
    #     back_populates='predecessor',
    #     lazy='selectin',
    #     cascade='all, delete-orphan',
    #     init=False
    # )

    # # Transitions where this plot is the successor (it replaced others)
    # transitions_as_successor: Mapped[List['PlotTransition']] = relationship(
    #     foreign_keys='PlotTransition.successor_id',
    #     back_populates='successor',
    #     lazy='selectin',
    #     cascade='all, delete-orphan',
    #     init=False
    # )

    protections: Mapped[List[PlotProtection]] = relationship(
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    note: Mapped[str] = mapped_column(String(500), default='')

    status: Mapped[PlotStatus] = mapped_column(default=PlotStatus.ACTIVE)

    def __repr__(self):
        return (
            f"Plot("
            f"slug={self.slug}, "
            f"estate={self.estate.slug}, "
            f"created_at={self.created_at}"
            ")"
        )

    @property
    def is_protected(self) -> bool:
        """Currently under any active protection."""
        now = datetime.now()
        return any(
            p.started_at <= now and (
                p.expires_at is None or p.expires_at >= now
            )
            for p in self.protections
        )

    @property
    def can_delete(self) -> bool:
        """Check if plot can be deleted."""
        return not any(
            p.blocks_deletion for p in self.protections
            if p.started_at <= datetime.now() <= (p.expires_at or datetime.max)
        )

from __future__ import annotations

from datetime import date, datetime
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
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
)

from agro_api.entities.base import BaseEntity
from config.database import table_registry
from config.geometry import GeometrySource

if TYPE_CHECKING:
    from agro_api.entities.activity import Activity
    from agro_api.entities.core import User
    from agro_api.entities.estate import Estate
    from agro_api.entities.field import FieldProtection, FieldTransition
    from agro_api.entities.soil import SoilType


# Pode ser removido:
# ACTIVE ocorre quando active_to for NULL
# INACTIVE quando active_to estiver no passado e não tiver transitions
# TRANSITIONED quando tiver transitions
class FieldStatus(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    TRANSITIONED = 'transitioned'


@mapped_as_dataclass(table_registry)
class Field(BaseEntity):
    __tablename__ = 'fields'
    __table_args__ = (
        UniqueConstraint('estate_id', 'slug', name='idx_estate_field_slug'),
    )

    estate_id: Mapped[Uuid] = mapped_column(
        ForeignKey('estates.id', ondelete='CASCADE')
    )
    creator_id: Mapped[Uuid] = mapped_column(
        ForeignKey('users.id', ondelete='RESTRICT')
    )
    soil_type_id: Mapped[Uuid | None] = mapped_column(
        ForeignKey('soil_types.id', ondelete='RESTRICT'),
        comment="Soil type if different from the plot's predominant soil"
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
    description: Mapped[str | None] = mapped_column(String(200))

    boundary: Mapped[Geometry] = mapped_column(
        Geometry(
            geometry_type='POLYGON',
            spatial_index=True,
            srid=4326,
        ),
        nullable=False,  # Field must have a boundary
        comment="Field boundary polygon"
    )
    boundary_source: Mapped[GeometrySource | None]

    # Computed measurements (same pattern as Estate)
    calculated_area_m2: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),  # Slightly smaller than estate (fields are smaller)
        Computed("ST_Area(boundary::geography)",
            # """
            # CASE
            #     WHEN boundary IS NOT NULL
            #     THEN ST_Area(boundary::geography)
            #     ELSE NULL
            # END
            # """,
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

    creator: Mapped['User'] = relationship()
    estate: Mapped['Estate'] = relationship(
        back_populates='fields', lazy='joined'
    )
    activities: Mapped[List['Activity']] = relationship(
        back_populates='field',
        cascade='all, delete-orphan',
        init=False
    )
    soil_type: Mapped['SoilType'] = relationship(lazy='joined')

    transitions_as_predecessor: Mapped[List['FieldTransition']] = relationship(
        foreign_keys='FieldTransition.predecessor_id',
        back_populates='predecessor',
        lazy='selectin',
        cascade='all, delete-orphan',
        init=False,
        comment="""
        Transitions where this field is the predecessor (it was replaced)
        """
    )

    transitions_as_successor: Mapped[List['FieldTransition']] = relationship(
        foreign_keys='FieldTransition.successor_id',
        back_populates='successor',
        lazy='selectin',
        cascade='all, delete-orphan',
        init=False,
        comment="""
        Transitions where this field is the successor (it replaced others)
        """
    )

    protections: Mapped[List['FieldProtection']] = relationship(
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    note: Mapped[str] = mapped_column(String(500), default='')

    status: Mapped[FieldStatus] = mapped_column(default=FieldStatus.ACTIVE)

    def __repr__(self):
        return (
            f"Field("
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
        """Check if field can be deleted."""
        return not any(
            p.blocks_deletion for p in self.protections
            if p.started_at <= datetime.now() <= (p.expires_at or datetime.max)
        )

    @property
    def is_active(self) -> bool:
        return self.active_to is None

    @property
    def is_inactive(self) -> bool:
        return self.active_to is not None and not self.is_transitioned

    @property
    def is_transitioned(self) -> bool:
        return len(self.transitions_as_predecessor) > 0

    @property
    def is_successor(self) -> bool:
        return len(self.transitions_as_predecessor) > 0

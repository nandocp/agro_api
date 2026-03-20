from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING, List
from uuid import UUID

from geoalchemy2 import Geometry
from sqlalchemy import (
    Computed,
    Date,
    ForeignKey,
    Numeric,
    String,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.model import BaseModel

if TYPE_CHECKING:
    from app.domain.accounts.models import User
    from app.domain.activities.models import Activity
    from app.domain.estates.models import Estate
    from app.domain.fields.models import (
        FieldProtection,
        FieldSoilAnalysis,
        FieldTransition,
        SoilClassification,
    )


class Field(BaseModel):
    __tablename__ = 'fields'
    __table_args__ = (
        UniqueConstraint('estate_id', 'slug', name='uq_estate_field_slug'),
    )

    estate_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey('estates.id', ondelete='CASCADE'), nullable=False
    )
    creator_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey('users.id', ondelete='RESTRICT'), nullable=False
    )

    slug: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        comment='URL-safe identifier within Estate',
    )

    label: Mapped[str] = mapped_column(
        String(96), comment='Human-readable name', nullable=False
    )

    notes: Mapped[str | None] = mapped_column(
        String(500), default=None, nullable=True
    )

    boundary: Mapped[Geometry | None] = mapped_column(
        Geometry(
            geometry_type='POLYGON',
            spatial_index=False,
            srid=4326,
        ),
        nullable=True,
        default=None,
        comment='Field boundary polygon',
    )
    boundary_source: Mapped[str | None] = mapped_column(
        String(32), default=None, nullable=True
    )

    calculated_area_m2: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        Computed('ST_Area(boundary::geography)', persisted=True),
        init=False,
        nullable=True,
        comment='Computed measurement',
    )

    perimeter_m: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        Computed('ST_Perimeter(boundary::geography)', persisted=True),
        nullable=True,
        init=False,
        comment='Computed measurement',
    )

    # Temporal validity (zones can be split, merged, or retired)
    active_from: Mapped[date] = mapped_column(
        Date, server_default=func.current_date(), nullable=False
    )
    active_to: Mapped[date | None] = mapped_column(
        Date,
        comment='NULL means currently active',
        init=False,
        default=None,
        nullable=True,
    )

    # Soil slope data
    slope_percent: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
        default=None,
        comment='Slope in percent: measured or estimated',
    )
    slope_class: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        default=None,
        comment=(
            'SlopeClass enum: classified automatically '
            'if slope_percent informed'
        ),
    )
    creator: Mapped['User'] = relationship('User', lazy='raise', init=False)
    estate: Mapped['Estate'] = relationship(
        'Estate', back_populates='fields', lazy='raise'
    )
    activities: Mapped[List['Activity']] = relationship(
        'Activity',
        back_populates='field',
        cascade='all, delete-orphan',
        init=False,
        lazy='raise',
    )
    protections: Mapped[List['FieldProtection']] = relationship(
        lazy='raise', cascade='all, delete-orphan', init=False
    )
    soil_analyses: Mapped[List['FieldSoilAnalysis']] = relationship(
        'FieldSoilAnalysis', back_populates='field', lazy='raise'
    )
    soil_classifications: Mapped[List['SoilClassification']] = relationship(
        'SoilClassification',
        secondary='field_soil_classifications',
        lazy='raise',
        init=False,
    )
    # Transitions where this field is the predecessor (it was replaced)
    transitions_as_predecessor: Mapped[List['FieldTransition']] = relationship(
        'FieldTransition',
        foreign_keys='FieldTransition.predecessor_id',
        back_populates='predecessor',
        lazy='raise',
        cascade='all, delete-orphan',
        init=False,
    )

    # Transitions where this field is the successor (it replaced others)
    transitions_as_successor: Mapped[List['FieldTransition']] = relationship(
        'FieldTransition',
        foreign_keys='FieldTransition.successor_id',
        back_populates='successor',
        lazy='raise',
        cascade='all, delete-orphan',
        init=False,
    )

    def __repr__(self):
        return (
            f'Field('
            f'id={self.id}, '
            f'slug={self.slug}, '
            f'estate={self.estate.slug}, '
            f'created_at={self.created_at}'
            ')'
        )

    @property
    def is_active(self) -> bool:
        return self.active_to is None

    @property
    def is_protected(self) -> bool:
        """Currently under any active protection."""
        now = datetime.now()
        return any(
            p.started_at <= now
            and (p.expires_at is None or p.expires_at >= now)
            for p in self.protections
        )

    # @property
    # def can_delete(self) -> bool:
    #     """Check if field can be deleted."""
    #     return not any(
    #         p.blocks_deletion
    #         for p in self.protections
    #         if p.started_at <= datetime.now() <=
    # (p.expires_at or datetime.max)
    #     )

    # @property
    # def is_inactive(self) -> bool:
    #     return self.active_to is not None and not self.is_transitioned

    # @property
    # def is_transitioned(self) -> bool:
    #     return len(self.transitions_as_predecessor) > 0

    # @property
    # def is_successor(self) -> bool:
    #     return len(self.transitions_as_predecessor) > 0

    # drainage_class: Mapped[str | None] = mapped_column(String(50))
    # slope_percent: Mapped[float | None] = mapped_column(
    #     Numeric(5, 2),
    #     comment='Soil slope in percentage'
    # )
    # soil_type: Mapped['SoilType'] = relationship(lazy='joined')

    # soil_type_id: Mapped[Uuid | None] = mapped_column(
    #     ForeignKey('soil_types.id', ondelete='RESTRICT'),
    #     comment="Soil type if different from the plot's predominant soil",
    # )

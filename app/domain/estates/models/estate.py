from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING, List
from uuid import UUID

from geoalchemy2 import Geometry
from sqlalchemy import (
    CheckConstraint,
    Computed,
    Date,
    ForeignKey,
    Numeric,
    String,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.estates.enums import EstateStatus, EstateZone, OwnershipType
from app.shared.model import BaseModel

if TYPE_CHECKING:
    from app.domain.accounts.models import Account
    from app.domain.estates.models import EstateRegistry
    from app.domain.fields.models import Field
    from app.shared.address.model import Address


class Estate(BaseModel):
    __tablename__ = 'estates'
    __table_args__ = (
        UniqueConstraint('account_id', 'slug', name='uq_account_estate_slug'),
        CheckConstraint(
            'declared_area_m2 IS NULL OR declared_area_m2 > 0',
            name='ck_estate_positive_declared_area',
        ),
    )

    account_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False
    )

    address_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey('addresses.id', ondelete='SET NULL'),
        nullable=True,
        init=False,
        default=None,
    )

    # Dates important to Estate management
    opened_at: Mapped[date | None] = mapped_column(
        Date, default=None, nullable=True
    )
    archived_at: Mapped[date | None] = mapped_column(
        Date, default=None, nullable=True, init=False
    )

    # Estate common data
    label: Mapped[str] = mapped_column(
        String(96), init=True, comment='Human-readable name'
    )
    slug: Mapped[str] = mapped_column(
        String(64), nullable=False, index=True, comment='URL-safe identifier'
    )
    description: Mapped[str | None] = mapped_column(
        String(200), default=None, nullable=True, init=False
    )
    timezone: Mapped[str] = mapped_column(
        String(64), default='America/Sao_Paulo', nullable=False
    )
    zone: Mapped[str] = mapped_column(
        String(16),
        default=EstateZone.RURAL.value,
        nullable=False,
        comment='Geographic location',
    )
    usage: Mapped[str | None] = mapped_column(
        String(50),
        default=None,
        nullable=True,
        comment='Predominant usage — family_farm, extractive, etc',
    )
    status: Mapped[str] = mapped_column(
        String(50), default=EstateStatus.ACTIVE, nullable=False
    )
    ownership_type: Mapped[str] = mapped_column(
        String(50), default=OwnershipType.OWNED.value, nullable=False
    )
    declared_area_m2: Mapped[Decimal | None] = mapped_column(
        Numeric(14, 2), nullable=True, default=None
    )

    # Geometry data
    entrance_point: Mapped[Geometry | None] = mapped_column(
        Geometry(geometry_type='POINT', srid=4326, spatial_index=False),
        default=None,
        nullable=True,
        comment='Estate access location (geographic data)',
    )
    boundary: Mapped[Geometry | None] = mapped_column(
        Geometry(geometry_type='MULTIPOLYGON', srid=4326, spatial_index=False),
        default=None,
        nullable=True,
        comment='Always 4326 (universal exchange format)',
    )
    boundary_source: Mapped[str | None] = mapped_column(
        String(32), default=None, nullable=True
    )

    # Calculated data from Geometries
    perimeter_m: Mapped[Decimal | None] = mapped_column(
        Numeric(14, 2),
        Computed(
            """
            CASE
                WHEN boundary IS NOT NULL
                THEN ST_Perimeter(boundary::geography)
                ELSE NULL
            END
            """,
            persisted=True,
        ),
        init=False,
        default=None,
        nullable=True,
        comment='Automatically updated when boundary changes',
    )
    calculated_area_m2: Mapped[Decimal | None] = mapped_column(
        Numeric(14, 2),
        Computed(
            """
            CASE
                WHEN boundary IS NOT NULL
                THEN ST_Area(boundary::geography)
                ELSE NULL
            END
            """,
            persisted=True,
        ),
        init=False,
        default=None,
        nullable=True,
        comment='Automatically updated when boundary changes',
    )

    # Relationships
    address: Mapped['Address'] = relationship(
        'Address', lazy='raise', foreign_keys=[address_id], init=False
    )
    account: Mapped['Account'] = relationship(
        'Account',
        back_populates='estates',
        lazy='raise',
        passive_deletes=True,
        init=False,
    )
    registries: Mapped[List['EstateRegistry']] = relationship(
        'EstateRegistry',
        back_populates='estate',
        cascade='all, delete-orphan',
        lazy='raise',
        init=False,
    )
    fields: Mapped[List['Field']] = relationship(
        'Field', back_populates='estate', init=False, lazy='raise'
    )

    def __repr__(self):
        return (
            f'Estate('
            f'id={self.id}, '
            f'slug={self.slug}, '
            f'status={self.status.value if self.status else None}, '
            f'created_at={self.created_at}'
            ')'
        )

    @property
    def is_urban(self):
        return 'urban' in self.kind.value

    @property
    def area_ha(self) -> Decimal | None:
        if self.calculated_area_m2 is None:
            return None

        return self.calculated_area_m2 / 10000

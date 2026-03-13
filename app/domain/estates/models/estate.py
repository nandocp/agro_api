from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from geoalchemy2 import Geometry
from sqlalchemy import (
    CheckConstraint,
    Computed,
    ForeignKey,
    Numeric,
    String,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.estates.enums import EstateKind, EstateStatus, OwnershipType
from app.shared.geometry import GeometrySource
from app.shared.model import BaseModel

if TYPE_CHECKING:
    from app.domain.accounts import Account
#     from app.entities.estate import EstateRegistry
#     from app.entities.field import Field


class Estate(BaseModel):
    __tablename__ = 'estates'
    __table_args__ = (
        UniqueConstraint('account_id', 'slug', name='idx_account_estate_slug'),
        CheckConstraint(
            'declared_area_m2 IS NULL OR declared_area_m2 > 0',
            name='ck_estate_positive_declared_area',
        ),
    )

    account_id: Mapped[Uuid] = mapped_column(
        ForeignKey('accounts.id', ondelete='CASCADE')
    )

    # Dates important to Estate management
    opened_at: Mapped[date | None] = mapped_column(nullable=True)
    deleted_at: Mapped[date | None] = mapped_column(default=None)

    # Estate common data
    label: Mapped[str] = mapped_column(
        String(96), init=True, comment='Human-readable name'
    )
    slug: Mapped[str] = mapped_column(
        String(64), nullable=False, index=True, comment='URL-safe identifier'
    )
    description: Mapped[str | None] = mapped_column(String(200), default=None)
    timezone: Mapped[str] = mapped_column(default='America/Sao_Paulo')
    kind: Mapped[EstateKind] = mapped_column(default=EstateKind.RURAL)
    status: Mapped[EstateStatus] = mapped_column(default=EstateStatus.ACTIVE)
    ownership_type: Mapped[OwnershipType] = mapped_column(
        default=OwnershipType.MANAGED
    )
    declared_area_m2: Mapped[Decimal | None] = mapped_column(
        Numeric(16, 2), nullable=True, default=None
    )

    # Geometry data
    entrance_point: Mapped[Geometry | None] = mapped_column(
        Geometry(geometry_type='POINT', srid=4326, spatial_index=False),
        default=None,
        comment='Estate access location (geographic data)',
    )
    boundary: Mapped[Geometry | None] = mapped_column(
        Geometry(geometry_type='MULTIPOLYGON', srid=4326, spatial_index=False),
        default=None,
        comment='Always 4326 (universal exchange format)',
    )
    boundary_source: Mapped[GeometrySource | None] = mapped_column(
        default=None
    )

    # Calculated data from Geometries
    perimeter_m: Mapped[Decimal | None] = mapped_column(
        Numeric(16, 2),
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
        comment='Automatically updated when boundary changes',
    )
    calculated_area_m2: Mapped[Decimal | None] = mapped_column(
        Numeric(16, 2),
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
        comment='Automatically updated when boundary changes',
    )

    # Relationships
    # address: Mapped['Address'] = relationship(
    #     back_populates='estate', lazy='joined', passive_deletes=True
    # )
    account: Mapped['Account'] = relationship(
        back_populates='estates', lazy='joined', passive_deletes=True
    )
    # fields: Mapped[List['Field']] = relationship(
    #     back_populates='estate', init=False, lazy='dynamic'
    # )
    # registries: Mapped[List['EstateRegistry']] = relationship(
    #     back_populates='estate',
    #     cascade='all, delete-orphan',
    #     lazy='joined',
    #     init=False,
    # )

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

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, List

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
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
)

from agro_api.entities.base import BaseEntity
from agro_api.entities.estate import EstateKind, EstateStatus
from config.database import table_registry
from config.geometry import GeometrySource

if TYPE_CHECKING:
    from agro_api.entities.core import Account
    from agro_api.entities.field import Field


@mapped_as_dataclass(table_registry, kw_only=True)
class Estate(BaseEntity):
    __tablename__ = 'estates'
    __table_args__ = (
        UniqueConstraint('account_id', 'slug', name='idx_account_estate_slug'),
        CheckConstraint(
            """
            registry_codes IS NULL OR(
                jsonb_typeof(registry_codes) = 'object'
                AND NOT registry_codes ? ''
            )
            """,
            name='ck_estate_registry_codes_structure',
        ),
        CheckConstraint(
            'declared_area_m2 IS NULL OR declared_area_m2 > 0',
            name='ck_estate_positive_declared_area',
        ),
    )

    account_id: Mapped[Uuid] = mapped_column(
        ForeignKey('accounts.id', ondelete='CASCADE')
    )

    opened_at: Mapped[datetime | None] = mapped_column(nullable=True)
    deleted_at: Mapped[datetime | None] = mapped_column(default=None)

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

    label: Mapped[str] = mapped_column(
        String(96), init=True, comment='Human-readable name'
    )

    slug: Mapped[str] = mapped_column(
        String(64), nullable=False, index=True, comment='URL-safe identifier'
    )

    description: Mapped[str | None] = mapped_column(String(200), default=None)

    account: Mapped['Account'] = relationship(
        back_populates='estates', lazy='joined', passive_deletes=True
    )

    fields: Mapped[List['Field']] = relationship(
        back_populates='estate', init=False, lazy='dynamic'
    )

    registry_codes: Mapped[dict | None] = mapped_column(
        MutableDict.as_mutable(JSONB),  # Tracks in-place changes
        nullable=True,
    )

    declared_area_m2: Mapped[Decimal | None] = mapped_column(
        Numeric(16, 2), nullable=True, default=None
    )

    entrance_point: Mapped[Geometry | None] = mapped_column(
        Geometry(
            geometry_type='POINT',
            spatial_index=True,
            srid=4326,
        ),
        default=None,
        comment='Estate access location (geographic data)',
    )
    boundary: Mapped[Geometry | None] = mapped_column(
        Geometry(
            geometry_type='MULTIPOLYGON',
            spatial_index=True,
            srid=4326,
        ),
        default=None,
        comment='Always 4326 (universal exchange format)',
    )

    boundary_source: Mapped[GeometrySource | None] = mapped_column(
        default=None
    )

    timezone: Mapped[str] = mapped_column(default='America/Sao_Paulo')

    kind: Mapped[EstateKind] = mapped_column(default=EstateKind.RURAL)

    status: Mapped[EstateStatus] = mapped_column(default=EstateStatus.ACTIVE)

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

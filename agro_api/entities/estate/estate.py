from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum
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
from config.database import table_registry
from config.geometry import GeometrySource

if TYPE_CHECKING:
    from agro_api.entities.core import Account
    from agro_api.entities.field import Field


class EstateKind(str, Enum):
    RURAL = 'rural'
    INTRAURBAN = 'intraurban'
    PERIURBAN = 'periurban'


class OwnershipType(str, Enum):
    OWNED = 'owned'
    LEASED = 'leased'
    MANAGED = 'managed'


class EstateStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending_validation"
    ARCHIVED = "archived"


@mapped_as_dataclass(table_registry)
class Estate(BaseEntity):
    __tablename__ = 'estates'
    __table_args__ = (
        UniqueConstraint('account_id', 'slug', name='idx_estate_account_slug'),
        # Ensures that what is stored is either NULL or a JSON object
        CheckConstraint(
            """
            registry_codes IS NULL OR(
                jsonb_typeof(registry_codes) = 'object'
                AND NOT registry_codes ? ''
            )
            """,
            name='ck_estate_registry_codes_structure'
        ),
        CheckConstraint(
            'declared_area_m2 IS NULL OR declared_area_m2 > 0',
            name='ck_estate_declared_area_positive'
        ),
    )

    account_id: Mapped[Uuid] = mapped_column(
        ForeignKey('accounts.id', ondelete='CASCADE')
    )

    # boundary_quality: Mapped[GeometryQuality | None] = mapped_column(
    #     comment="high/medium/low - confidence in boundary accuracy"
    # )

    perimeter_m: Mapped[Decimal] = mapped_column(
        Numeric(16, 2),
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
        nullable=True,
        init=False
    )

    calculated_area_m2: Mapped[Decimal] = mapped_column(
        Numeric(16, 2),
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
        nullable=True,
        init=False,
        comment="Automatically updated when boundary changes"
    )

    label: Mapped[str] = mapped_column(
        String(96),
        comment='Human-readable name'
    )

    slug: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True,
        comment='URL-safe identifier'
    )

    description: Mapped[str | None]

    started_at: Mapped[datetime] = mapped_column(nullable=True)

    account: Mapped['Account'] = relationship(
        back_populates='estates', lazy='joined', passive_deletes=True
    )

    fields: Mapped[List['Field']] = relationship(
        back_populates='estate', init=False, lazy='dynamic'
    )

    ownership_type: Mapped[OwnershipType] = mapped_column(nullable=True)

    registry_codes: Mapped[dict | None] = mapped_column(
        MutableDict.as_mutable(JSONB),  # Tracks in-place changes
        nullable=True
    )

    declared_area_m2: Mapped[Decimal | None] = mapped_column(
        Numeric(16, 2), nullable=True, default=None
    )

    deleted_at: Mapped[datetime | None] = mapped_column(default=None)

    # GEOGRAPHIC DATA
    entrance_point: Mapped[Geometry | None] = mapped_column(
        Geometry(
            geometry_type='POINT',
            spatial_index=True,
            srid=4326,
        ),
        default=None,
        comment='Estate access location'
    )
    # STORAGE: Always 4326 (universal exchange format)
    boundary: Mapped[Geometry | None] = mapped_column(
        Geometry(
            geometry_type='MULTIPOLYGON',
            spatial_index=True,
            srid=4326,
        ),
        default=None
    )

    boundary_source: Mapped[GeometrySource | None] = mapped_column(
        default=None
    )

    timezone: Mapped[str] = mapped_column(default='America/Sao_Paulo')

    kind: Mapped[EstateKind] = mapped_column(default=EstateKind.RURAL)

    status: Mapped[EstateStatus] = mapped_column(default=EstateStatus.ACTIVE)


    def __repr__(self):
        return (
            f"Estate("
            f"id={self.id}, "
            f"slug={self.slug}, "
            f"status={self.status.value if self.status else None}, "
            f"created_at={self.created_at}"
            ")"
        )

    @property
    def is_urban(self):
        return 'urban' in self.kind.value

    @property
    def area_ha(self) -> Decimal | None:
        if self.calculated_area_m2 is None:
            return None

        return self.calculated_area_m2 / 10000

    # # Store number of polygons (if MULTIPOLYGON)
    # Set this as property, to be used when needed (don't think will be)
    # polygon_count: Mapped[int] = mapped_column(
    #     Computed(
    #         """
    #         CASE
    #             WHEN boundary IS NOT NULL
    #             THEN ST_NumGeometries(boundary)
    #             ELSE NULL
    #         END
    #         """,
    #         persisted=True
    #     ),
    #     nullable=True
    # )

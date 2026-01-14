from __future__ import annotations

from datetime import datetime

from geoalchemy2 import Geometry
from sqlalchemy import ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    # relationship,
)

from config.database import table_registry


@mapped_as_dataclass(table_registry)
class Geo:
    __tablename__ = 'estate_geos'

    id: Mapped[Uuid] = mapped_column(
        UUID,
        init=False,
        primary_key=True,
        server_default=func.gen_random_uuid(),
        nullable=False,
    )

    estate_id: Mapped[Uuid] = mapped_column(ForeignKey('estates.id'))

    coordinates: Mapped[Geometry] = mapped_column(
        Geometry(
            geometry_type='POINT',
            srid=4326,
            spatial_index=True,
        ),
        nullable=False,
        init=True,
    )

    limits: Mapped[Geometry] = mapped_column(
        Geometry(
            geometry_type='POLYGON',
            srid=4326,
            spatial_index=True,
        ),
        nullable=False,
        init=True,
    )

    projection_srid: Mapped[int]

    total_area_m2: Mapped[float] = mapped_column(init=False)

    is_protected: Mapped[bool]

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    # surface: Mapped[Geometry] = mapped_column(
    #     Geometry(
    #         geometry_type='TIN',
    #         srid=4326,
    #     ),
    #     nullable=True
    # )

    # estate = relationship(
    # 'Estate', back_populates='geo_data', lazy='selectin')

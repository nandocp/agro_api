from datetime import datetime

from geoalchemy2 import Geometry
from sqlalchemy import ForeignKey, UniqueConstraint, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column

from agro_api.entities.base import table_registry


@mapped_as_dataclass(table_registry)
class EstateDivision:
    __tablename__ = 'estates_divisions'
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

    estate_id: Mapped[Uuid] = mapped_column(ForeignKey('estate.id'))

    label: Mapped[str] = mapped_column(unique=False)

    slug: Mapped[str] = mapped_column(nullable=False)

    limits: Mapped[Geometry] = mapped_column(
        Geometry(
            geometry_type='MULTIPOLYGON',
            srid=4326,
            spatial_index=True,
        ),
        nullable=True,
        init=False,
    )

    divided_at: Mapped[datetime] = mapped_column(
        init=False, nullable=True, server_default=func.now()
    )

    merged_at: Mapped[datetime] = mapped_column(init=False, nullable=True)

    is_active: Mapped[bool] = mapped_column(init=False, default=True)

    def __repr__(self):
        return f'<EstateDivision(slug={self.slug}, area={self.area()})>'

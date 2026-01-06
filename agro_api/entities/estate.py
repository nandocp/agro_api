from datetime import datetime
from enum import Enum

from geoalchemy2 import Geometry
from sqlalchemy import ForeignKey, UniqueConstraint, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column

from agro_api.entities.base import table_registry
from config.geometry import wkb_to_shape


class EstateKind(Enum):
    rural = 'rural'
    intraurban = 'intraurban'
    periurban = 'periurban'


@mapped_as_dataclass(table_registry)
class Estate:
    __tablename__ = 'estates'
    __table_args__ = (
        UniqueConstraint('user_id', 'slug'),
    )

    id: Mapped[Uuid] = mapped_column(
        UUID,
        init=False,
        primary_key=True,
        server_default=func.gen_random_uuid(),
        nullable=False,
    )

    user_id: Mapped[Uuid] = mapped_column(ForeignKey('users.id'))

    label: Mapped[str] = mapped_column(unique=False)

    slug: Mapped[str] = mapped_column(unique=True, nullable=False)

    coordinates: Mapped[Geometry] = mapped_column(
        Geometry(
            geometry_type='POINT',
            srid=4326,
            spatial_index=True,
        ),
        nullable=True,
        init=False,
    )

    limits: Mapped[Geometry] = mapped_column(
        Geometry(
            geometry_type='MULTIPOLYGON',
            srid=4326,
            spatial_index=True,
        ),
        nullable=True,
        init=False,
    )

    opened_at: Mapped[datetime] = mapped_column(
        nullable=True, server_default=func.now()
    )

    closed_at: Mapped[datetime] = mapped_column(init=False, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    kind: Mapped[EstateKind] = mapped_column(default=EstateKind('rural'))

    def area(self):
        if not self.limits:
            return None

        shape = wkb_to_shape(self.limits)
        return f'{shape.area:.2f}'

    def is_urban(self):
        return 'urban' in self.kind.value

    def __repr__(self):
        return f'<Estate(slug={self.slug}, area={self.area()})>'

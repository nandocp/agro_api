from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, UniqueConstraint, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
)

from agro_api.entities.base import table_registry


class EstateKind(str, Enum):
    rural = 'rural'
    intraurban = 'intraurban'
    periurban = 'periurban'


@mapped_as_dataclass(table_registry)
class Estate:
    __tablename__ = 'estates'
    __table_args__ = (UniqueConstraint('user_id', 'slug'),)

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

    description: Mapped[str]

    opened_at: Mapped[datetime] = mapped_column(
        nullable=True, server_default=func.now()
    )

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    kind: Mapped[EstateKind] = mapped_column(default=EstateKind.rural)

    user = relationship('User', init=False, back_populates='estates')

    plots = relationship(
        'Plot', init=False, back_populates='estate', lazy='selectin'
    )

    geo_data = relationship(
        'Geo', init=False, back_populates='estate', lazy='selectin'
    )

    def is_urban(self):
        return 'urban' in self.kind.value

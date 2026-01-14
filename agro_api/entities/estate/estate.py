from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Set

from sqlalchemy import ForeignKey, UniqueConstraint, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
)

from config.database import table_registry

if TYPE_CHECKING:
    from agro_api.entities.core import Account
    from agro_api.entities.estate import Plot


class EstateKind(str, Enum):
    rural = 'rural'
    intraurban = 'intraurban'
    periurban = 'periurban'


@mapped_as_dataclass(table_registry)
class Estate:
    __tablename__ = 'estates'
    __table_args__ = (UniqueConstraint('account_id', 'slug'),)

    id: Mapped[Uuid] = mapped_column(
        UUID,
        init=False,
        primary_key=True,
        server_default=func.gen_random_uuid(),
        nullable=False,
    )

    account_id: Mapped[Uuid] = mapped_column(ForeignKey('accounts.id'))

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

    account: Mapped['Account'] = relationship(
        back_populates='estates', init=False, lazy='selectin'
    )

    plots: Mapped[Set['Plot']] = relationship(
        back_populates='estate', init=False, lazy='selectin'
    )

    # geo_data = relationship(
    #     back_populates='estate', init=False, lazy='selectin'
    # )

    def is_urban(self):
        return 'urban' in self.kind.value

    def __repr__(self):
        repr_attrs = [
            f'id={self.id}',
            f'slug={self.slug}',
            f'created_at={self.created_at}'
        ]
        return f'Estate({(', '.join(repr_attrs))})'

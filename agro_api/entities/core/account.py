from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
)

from config.database import table_registry

if TYPE_CHECKING:
    from agro_api.entities.core import User
    from agro_api.entities.estate import Estate


@mapped_as_dataclass(table_registry)
class Account:
    __tablename__ = 'accounts'

    id: Mapped[Uuid] = mapped_column(
        UUID,
        init=False,
        primary_key=True,
        server_default=func.gen_random_uuid(),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(unique=False)

    document: Mapped[str] = mapped_column(unique=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    deleted_at: Mapped[datetime] = mapped_column(init=False, nullable=True)

    users: Mapped[List['User']] = relationship(
        back_populates='account',
        init=False,
        cascade='all, delete-orphan',
        lazy='selectin'
    )

    estates: Mapped[List['Estate']] = relationship(
        back_populates='account',
        init=False,
        cascade='all, delete-orphan',
        lazy='selectin'
    )

    def __repr__(self):
        return f'Account(id={self.id}, name={self.name})'

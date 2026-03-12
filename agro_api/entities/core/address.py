from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
)

from agro_api.entities.base import BaseEntity
from config.database import table_registry

if TYPE_CHECKING:
    from agro_api.entities.estate import Estate


@mapped_as_dataclass(table_registry)
class Address(BaseEntity):
    __tablename__ = 'addresses'

    # Core address fields
    street: Mapped[str | None]
    number: Mapped[str | None]
    complement: Mapped[str | None]
    neighborhood: Mapped[str | None]
    city: Mapped[str]
    state: Mapped[str]
    postal_code: Mapped[str | None]
    country: Mapped[str] = mapped_column(String(3), default='BRA')

    # Relationships
    estate: Mapped['Estate'] = relationship(back_populates='address')

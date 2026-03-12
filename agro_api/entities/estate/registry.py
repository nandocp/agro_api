from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
)

from agro_api.entities.base import BaseEntity
from agro_api.entities.estate import RegistryStatus
from config.database import table_registry

if TYPE_CHECKING:
    from agro_api.entities.estate import Estate, RegistryStatus


@mapped_as_dataclass(table_registry, kw_only=True)
class EstateRegistry(BaseEntity):
    """Códigos de registro de uma propriedade rural em diferentes órgãos."""

    __tablename__ = 'estate_registries'
    __table_args__ = (
        UniqueConstraint('estate_id', 'code', name='uq_estate_registry_code'),
        Index('ix_estate_registry_code', 'code'),
        CheckConstraint(
            'length(trim(code)) > 0', name='ck_registry_code_not_empty'
        ),
    )

    estate_id: Mapped[Uuid] = mapped_column(
        ForeignKey('estates.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )

    code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment='Registration code with the competent public agency',
    )

    source: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        comment='Public agency/entity that issued the registration',
    )

    submitted_at: Mapped[date | None] = mapped_column()

    issued_at: Mapped[date | None] = mapped_column()

    expiry_date: Mapped[date | None] = mapped_column(default=None)

    notes: Mapped[str | None] = mapped_column(String(500))

    status: Mapped[RegistryStatus] = mapped_column(
        default=RegistryStatus.DRAFT
    )

    estate: Mapped['Estate'] = relationship(
        back_populates='registries', init=False
    )

    def __repr__(self):
        return (
            'EstateRegistry('
            f'estate={self.estate_id}, '
            f'source={self.source}, '
            f'code={self.code})'
        )

    @property
    def is_active(self):
        return self.status == RegistryStatus.ACTIVE

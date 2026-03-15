from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    Date,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.estates.enums import RegistryStatus
from app.shared.model import BaseModel

if TYPE_CHECKING:
    from app.domain.estates.models import Estate


class EstateRegistry(BaseModel):
    __tablename__ = 'estate_registries'
    __table_args__ = (
        UniqueConstraint(
            'estate_id', 'source', 'code', name='uq_estate_registry_code'
        ),
        Index('ix_estate_registry_code', 'code'),
        CheckConstraint(
            'length(trim(code)) > 0', name='ck_registry_code_not_empty'
        ),
    )

    estate_id: Mapped[UUID] = mapped_column(
        Uuid,
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
        String(128),
        nullable=False,
        comment='Public agency/entity that issued the registration',
    )

    submitted_at: Mapped[date | None] = mapped_column(
        Date, default=None, nullable=True
    )

    issued_at: Mapped[date | None] = mapped_column(
        Date, default=None, nullable=True
    )

    expires_at: Mapped[date | None] = mapped_column(
        Date, default=None, nullable=True
    )

    notes: Mapped[str | None] = mapped_column(
        String(500), default=None, nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(32), default=RegistryStatus.DRAFT, nullable=False
    )

    estate: Mapped['Estate'] = relationship(
        'Estate', back_populates='registries', init=False, lazy='raise'
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

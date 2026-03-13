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
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.estates.enums import RegistryStatus
from app.shared.model.base import BaseModel

if TYPE_CHECKING:
    from app.domain.estates.models import Estate


class EstateRegistry(BaseModel):
    __tablename__ = 'estate_registries'
    __table_args__ = (
        UniqueConstraint('estate_id', 'code', name='uq_estate_registry_code'),
        Index('ix_estate_registry_code', 'code'),
        CheckConstraint(
            'length(trim(code)) > 0', name='ck_registry_code_not_empty'
        ),
        CheckConstraint(
            (
                'expiry_date IS NULL OR '
                'issued_at IS NULL OR '
                'expiry_date >= issued_at'
            ),
            name='ck_registry_expiry_after_issued',
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
        comment='Registration code within the competent public agency/entity',
    )

    source: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        comment='Public agency/entity that issued the registration',
    )

    submitted_at: Mapped[date | None] = mapped_column(default=None)

    issued_at: Mapped[date | None] = mapped_column(default=None)

    expiry_date: Mapped[date | None] = mapped_column(default=None)

    notes: Mapped[str | None] = mapped_column(String(500), default=None)

    status: Mapped[RegistryStatus] = mapped_column(
        default=RegistryStatus.DRAFT, nullable=False
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

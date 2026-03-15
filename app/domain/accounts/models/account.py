from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List
from uuid import UUID

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.accounts.enums import AccountPlan
from app.shared.model import BaseModel

if TYPE_CHECKING:
    from app.domain.accounts.models import User
    from app.domain.estates.models import Estate


class Account(BaseModel):
    __tablename__ = 'accounts'
    __table_args__ = (
        UniqueConstraint('document', name='uq_account_document'),
    )

    address_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey('addresses.id', ondelete='SET NULL'),
        nullable=True,
        init=False,
        default=None,
    )

    name: Mapped[str] = mapped_column(
        String(128), unique=False, nullable=False
    )

    document: Mapped[str] = mapped_column(
        String(32), unique=True, nullable=False
    )

    plan: Mapped[str] = mapped_column(
        String(32), default=AccountPlan.FREE.value, nullable=False
    )

    archived_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), init=False, nullable=True, default=None
    )

    users: Mapped[List['User']] = relationship(
        'User',
        back_populates='account',
        init=False,
        cascade='all, delete-orphan',
        lazy='selectin',
    )

    estates: Mapped[List['Estate']] = relationship(
        'Estate',
        back_populates='account',
        init=False,
        cascade='all, delete-orphan',
        lazy='selectin',
    )

    def __repr__(self):
        return f'Account(id={self.id}, name={self.name})'

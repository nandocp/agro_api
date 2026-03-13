from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.accounts.enums import AccountPlan
from app.shared.model import BaseModel

if TYPE_CHECKING:
    from app.domain.accounts.models import User
    from app.domain.estates.models import Estate


class Account(BaseModel):
    __tablename__ = 'accounts'
    __table_args__ = (
        UniqueConstraint('document', name='idx_account_document'),
    )

    name: Mapped[str] = mapped_column(unique=False)

    document: Mapped[str] = mapped_column(unique=True, nullable=False)

    plan: Mapped[AccountPlan] = mapped_column(default=AccountPlan.FREE)

    deleted_at: Mapped[datetime | None] = mapped_column(
        init=False, nullable=True
    )

    users: Mapped[List['User']] = relationship(
        back_populates='account',
        init=False,
        cascade='all, delete-orphan',
        lazy='selectin',
    )

    estates: Mapped[List['Estate']] = relationship(
        back_populates='account',
        init=False,
        cascade='all, delete-orphan',
        lazy='selectin',
    )

    def __repr__(self):
        return f'Account(id={self.id}, name={self.name})'

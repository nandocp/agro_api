from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List
from uuid import UUID

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.model import BaseModel

if TYPE_CHECKING:
    from app.domain.accounts.models import Account, Role
    # from app.entities.activity import Activity


class User(BaseModel):
    __tablename__ = 'users'
    __table_args__ = (
        UniqueConstraint('account_id', 'email', name='uq_account_email'),
    )

    account_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    email: Mapped[str] = mapped_column(String(254), nullable=False)

    password: Mapped[str] = mapped_column(String(255), nullable=False)

    is_active: Mapped[bool] = mapped_column(
        Boolean, init=False, default=True, nullable=False
    )
    deactivated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), init=False, nullable=True
    )

    # Password reset
    reset_password_token: Mapped[str | None] = mapped_column(
        init=False, default=None, unique=True, nullable=True
    )
    reset_password_sent_at: Mapped[datetime | None] = mapped_column(
        init=False, default=None, nullable=True
    )

    # Session control
    jti: Mapped[UUID | None] = mapped_column(
        Uuid, init=False, nullable=True, unique=True, default=None
    )

    # Access history
    current_sign_in_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), init=False, default=None, nullable=True
    )
    last_sign_in_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), init=False, default=None, nullable=True
    )

    # Block on failed login attempts (wrong pwd)
    failed_attempts: Mapped[int] = mapped_column(
        Integer, init=False, default=0, nullable=False
    )
    locked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), init=False, default=None, nullable=True
    )
    unlock_token: Mapped[UUID | None] = mapped_column(
        Uuid, init=False, nullable=True, unique=True, default=None
    )

    # Relationships
    account: Mapped['Account'] = relationship(
        'Account', back_populates='users', init=False
    )
    roles: Mapped[List['Role']] = relationship(
        'Role',
        back_populates='users',
        secondary='user_roles',
        lazy='raise',
        init=False,
    )

    # created_activities: Mapped[List['Activity']] = relationship(
    #     back_populates='creator', init=False, lazy='raise
    # )

    def __repr__(self):
        return f'User(id={self.id}, name={self.name}, email={self.email})'

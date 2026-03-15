from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, UniqueConstraint, Uuid
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

    account_id: Mapped[Uuid] = mapped_column(
        ForeignKey('accounts.id', ondelete='CASCADE')
    )

    name: Mapped[str] = mapped_column(unique=False)

    email: Mapped[str] = mapped_column(nullable=False)

    password: Mapped[str] = mapped_column(nullable=False)

    is_active: Mapped[bool] = mapped_column(
        init=False, default=True, nullable=False
    )
    deactivated_at: Mapped[datetime] = mapped_column(init=False, nullable=True)

    # Password reset
    reset_password_token: Mapped[str | None] = mapped_column(
        init=False, default=None, unique=True
    )
    reset_password_sent_at: Mapped[datetime | None] = mapped_column(
        init=False, default=None
    )

    # Session control
    jti: Mapped[Uuid | None] = mapped_column(
        Uuid, init=False, nullable=True, unique=True, default=None
    )

    # Access history
    current_sign_in_at: Mapped[datetime | None] = mapped_column(
        init=False, default=None
    )
    last_sign_in_at: Mapped[datetime | None] = mapped_column(
        init=False, default=None
    )

    # Block on failed login attempts (wrong pwd)
    failed_attempts: Mapped[int] = mapped_column(
        init=False, default=0, nullable=False
    )
    locked_at: Mapped[datetime | None] = mapped_column(
        init=False, default=None
    )
    unlock_token: Mapped[Uuid | None] = mapped_column(
        Uuid, init=False, nullable=True, unique=True, default=None
    )

    account: Mapped['Account'] = relationship(
        back_populates='users', init=False
    )
    roles: Mapped[List['Role']] = relationship(
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

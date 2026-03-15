from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    Date,
    ForeignKey,
    Index,
    String,
    Uuid,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.model import BaseModel

if TYPE_CHECKING:
    from app.domain.accounts.models.user import User
    from app.domain.fields.models.field import Field


class FieldProtection(BaseModel):
    __tablename__ = 'field_protections'
    __table_args__ = (
        Index(  # Only one active protection per field at a time
            'ix_field_active_protection',
            'field_id',
            unique=True,
            postgresql_where=text('expires_at IS NULL'),
        ),
        CheckConstraint(
            'expires_at IS NULL OR expires_at > started_at',
            name='ck_field_protection_expiry',
        ),
    )

    field_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey('fields.id'), nullable=False
    )
    created_by_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey('users.id', ondelete='RESTRICT'), nullable=False
    )

    kind: Mapped[str] = mapped_column(String(32), nullable=False)
    reason: Mapped[str | None] = mapped_column(
        String(256),
        nullable=True,
        default=None,
        comment='What is the reason this field is protected, related to kind',
    )

    expires_at: Mapped[date | None] = mapped_column(
        Date, nullable=True, default=None
    )
    started_at: Mapped[date] = mapped_column(
        Date, server_default=func.current_date(), nullable=False
    )

    field: Mapped['Field'] = relationship(
        back_populates='protections',
        lazy='raise',
        init=False,
    )
    created_by: Mapped['User'] = relationship(
        lazy='raise',
        init=False,
    )

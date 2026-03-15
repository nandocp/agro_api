from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    String,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.fields.enums import FieldProtectionKind
from app.shared.model import BaseModel


class FieldProtection(BaseModel):
    __tablename__ = 'field_protections'
    __table_args__ = (
        UniqueConstraint(
            'field_id', 'protection_type', name='uq_field_protection'
        ),
        CheckConstraint(
            'expires_at IS NULL OR expires_at > started_at',
            name='ck_field_protection_expiry',
        ),
    )

    field_id: Mapped[Uuid] = mapped_column(ForeignKey('fields.id'))
    created_by_id: Mapped[Uuid] = mapped_column(ForeignKey('users.id'))

    kind: Mapped[FieldProtectionKind] = mapped_column(nullable=False)
    reason: Mapped[str | None] = mapped_column(String(256), nullable=True)

    expires_at: Mapped[datetime | None] = mapped_column(
        nullable=True, init=False
    )
    started_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False, init=False
    )

    # What operations are restricted
    blocks_deletion: Mapped[bool] = mapped_column(default=True)
    blocks_transition: Mapped[bool] = mapped_column(default=True)
    blocks_boundary_change: Mapped[bool] = mapped_column(default=False)

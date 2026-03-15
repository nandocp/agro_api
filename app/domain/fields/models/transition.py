from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    Date,
    ForeignKey,
    String,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.model import BaseModel

if TYPE_CHECKING:
    from app.domain.accounts.models import User
    from app.domain.fields.models import Field


"""Records all field changes over time."""


class FieldTransition(BaseModel):
    __tablename__ = 'field_transitions'
    __table_args__ = (
        UniqueConstraint(
            'predecessor_id',
            'successor_id',
            'kind',
            name='uq_field_transition',
        ),
        CheckConstraint(
            'predecessor_id != successor_id',
            name='ck_field_transition_no_self_reference',
        ),
    )

    predecessor_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey('fields.id', ondelete='RESTRICT'),
        nullable=False,
        index=True,
        comment='The field that existed before',
    )

    successor_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey('fields.id', ondelete='RESTRICT'),
        nullable=False,
        index=True,
        comment='The field that came after',
    )

    kind: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        comment='What kind of transition',
        init=True,
    )

    transitioned_at: Mapped[date] = mapped_column(
        Date,
        server_default=func.current_date(),
        nullable=False,
        comment='When the transition happened',
    )

    transitioned_by_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey('users.id', ondelete='SET NULL'),
        comment='User who performed the transition',
        init=False,
    )

    reason: Mapped[str | None] = mapped_column(
        String(500), nullable=True, default=None, init=False
    )

    # Relationships
    predecessor: Mapped['Field'] = relationship(
        'Field',
        foreign_keys=[predecessor_id],
        back_populates='transitions_as_predecessor',
        lazy='raise',
        init=False,
    )
    successor: Mapped['Field'] = relationship(
        'Field',
        foreign_keys=[successor_id],
        back_populates='transitions_as_successor',
        lazy='raise',
        init=False,
    )
    transitioned_by: Mapped['User'] = relationship('User', lazy='raise')

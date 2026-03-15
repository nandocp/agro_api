from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    String,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.fields.enums import FieldTransitionKind
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

    predecessor_id: Mapped[Uuid] = mapped_column(
        ForeignKey('fields.id', ondelete='RESTRICT'),
        nullable=False,
        index=True,
        comment='The field that existed before',
    )

    successor_id: Mapped[Uuid | None] = mapped_column(
        ForeignKey('fields.id', ondelete='RESTRICT'),
        nullable=False,
        index=True,
        comment='The field that came after',
    )

    kind: Mapped[FieldTransitionKind] = mapped_column(
        nullable=False, comment='What kind of transition'
    )

    transitioned_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
        comment='When the transition happened',
    )

    transitioned_by_id: Mapped[Uuid] = mapped_column(
        ForeignKey('users.id', ondelete='SET NULL'),
        comment='User who performed the transition',
        init=False,
    )

    reason: Mapped[str | None] = mapped_column(String(500), init=False)

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
    transitioned_by: Mapped['User'] = relationship(lazy='raise')

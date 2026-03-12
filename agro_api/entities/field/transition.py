"""Records all field changes over time."""

from datetime import datetime
from enum import Enum

from sqlalchemy import (
    ForeignKey,
    String,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
)

from agro_api.entities.base import BaseEntity
from agro_api.entities.core import User
from agro_api.entities.field import Field
from config.database import table_registry


class FieldTransitionType(str, Enum):
    MERGE = 'merge'  # Multiple fields → One field
    DIVIDE = 'divide'  # One field → Multiple fields
    BOUNDARY_ADJUST = 'boundary_adjust'  # Minor boundary change


@mapped_as_dataclass(table_registry)
class FieldTransition(BaseEntity):
    __tablename__ = 'field_transitions'
    __table_args__ = (
        # Ensure transition is not duplicated
        UniqueConstraint(
            'predecessor_id',
            'successor_id',
            'transition_type',
            name='uq_field_transition_unique',
        ),
    )

    # The field that existed before
    predecessor_id: Mapped[Uuid] = mapped_column(
        ForeignKey('fields.id', ondelete='RESTRICT'),
        nullable=False,
        index=True,
    )

    # The field that came after
    successor_id: Mapped[Uuid] = mapped_column(
        ForeignKey('fields.id', ondelete='RESTRICT'),
        nullable=False,
        index=True,
    )

    # What kind of transition
    transition_type: Mapped[FieldTransitionType] = mapped_column(
        nullable=False
    )

    # When it happened
    transitioned_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    # Optional: user who performed the transition
    transitioned_by_id: Mapped[Uuid | None] = mapped_column(
        ForeignKey('users.id', ondelete='SET NULL')
    )

    # Optional: notes about why
    reason: Mapped[str | None] = mapped_column(String(500))

    # Relationships
    # Field → transitions where it was predecessor
    predecessor: Mapped['Field'] = relationship(
        Field,
        foreign_keys=[predecessor_id],
        back_populates='transitions_as_predecessor',
    )
    # Field → transitions where it was successor
    successor: Mapped['Field'] = relationship(
        Field,
        foreign_keys=[successor_id],
        back_populates='transitions_as_successor',
    )
    transitioned_by: Mapped['User'] = relationship(lazy='joined')

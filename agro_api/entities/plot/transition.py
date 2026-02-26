"""Records all plot changes over time."""

from datetime import datetime
from enum import Enum

from sqlalchemy import (
    ForeignKey,
    String,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
)

from agro_api.entities.core import User
from agro_api.entities.plot import Plot
from config.database import table_registry


class PlotTransitionType(str, Enum):
    MERGE = 'merge'      # Multiple plots → One plot
    DIVIDE = 'divide'    # One plot → Multiple plots
    BOUNDARY_ADJUST = 'boundary_adjust'  # Minor boundary change


@mapped_as_dataclass(table_registry)
class PlotTransition:
    __tablename__ = 'plot_transitions'
    __table_args__ = (
        # Ensure transition is not duplicated
        UniqueConstraint(
            'predecessor_id', 'successor_id', 'transition_type',
            name='uq_plot_transition_unique'
        ),
    )

    id: Mapped[Uuid] = mapped_column(
        UUID,
        init=False,
        primary_key=True,
        server_default=func.uuidv7(),
        nullable=False,
    )

    # The plot that existed before
    predecessor_id: Mapped[Uuid] = mapped_column(
        ForeignKey('plots.id', ondelete='RESTRICT'),
        nullable=False,
        index=True
    )

    # The plot that came after
    successor_id: Mapped[Uuid] = mapped_column(
        ForeignKey('plots.id', ondelete='RESTRICT'),
        nullable=False,
        index=True
    )

    # What kind of transition
    transition_type: Mapped[PlotTransitionType] = mapped_column(nullable=False)

    # When it happened
    transitioned_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )

    # Optional: user who performed the transition
    transitioned_by_id: Mapped[Uuid | None] = mapped_column(
        ForeignKey('users.id', ondelete='SET NULL')
    )

    # Optional: notes about why
    reason: Mapped[str | None] = mapped_column(String(500))

    # Relationships
    # Plot → transitions where it was predecessor
    predecessor: Mapped[Plot] = relationship(
        Plot,
        foreign_keys=[predecessor_id],
        backref='transitions_as_predecessor'
    )
    # Plot → transitions where it was successor
    successor: Mapped[Plot] = relationship(
        Plot,
        foreign_keys=[successor_id],
        backref='transitions_as_successor'
    )
    transitioned_by: Mapped[User] = relationship(User, lazy='joined')

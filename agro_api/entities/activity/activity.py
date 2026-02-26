from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Numeric,
    String,
    Uuid,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
)

from agro_api.entities.base import BaseEntity
from config.database import table_registry

if TYPE_CHECKING:
    from agro_api.entities.core import User
    from agro_api.entities.plot import Plot


class ActivityStatus(str, Enum):
    PLANNED = 'planned'
    ACTIVE = 'active'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'


@mapped_as_dataclass(table_registry, kw_only=True)
class Activity(BaseEntity):
    __tablename__ = 'activities'
    __table_args__ = (
        CheckConstraint('finished_at IS NULL OR finished_at >= started_at'),
        CheckConstraint(
            'total_area_m2 IS NULL OR total_area_m2 > 0',
            name='ck_activity_area_positive'
        )
    )
    __mapper_args__ = {
        "polymorphic_identity": "activity",
        # discriminator: value indicate object type
        "polymorphic_on": 'activity_type',
    }

    activity_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Polymorphic discriminator: planting, grazing, processing..."
    )
    plot_id: Mapped[Uuid] = mapped_column(
        ForeignKey('plots.id'), index=True, nullable=False
    )
    creator_id: Mapped[Uuid] = mapped_column(
        ForeignKey('users.id'), nullable=False
    )
    parent_id: Mapped[Uuid | None] = mapped_column(
        ForeignKey('activities.id'),
        index=True
    )

    # Batch/group identifier
    batch_id: Mapped[Uuid | None] = mapped_column(index=True)

    # Common fields
    started_at: Mapped[datetime] = mapped_column(index=True)
    finished_at: Mapped[datetime | None]
    total_area_m2: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        comment="Area this activity covers (validate against plot area)"
    )

    notes: Mapped[str | None]
    status: Mapped[ActivityStatus] = mapped_column(
        default=ActivityStatus.PLANNED, nullable=False
    )

    # Relationships
    creator: Mapped[User] = relationship(
        back_populates='created_activities', init=False
    )
    plot: Mapped[Plot] = relationship(
        back_populates='activities', init=False
    )
    # For hierarchies
    parent: Mapped[Activity] = relationship(
        remote_side='Activity.id',
        foreign_keys=[parent_id],
        init=False
    )

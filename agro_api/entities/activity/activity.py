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
    from agro_api.entities.field import Field


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

    field_id: Mapped[Uuid] = mapped_column(
        ForeignKey('fields.id'), index=True, nullable=False
    )
    creator_id: Mapped[Uuid] = mapped_column(
        ForeignKey('users.id'), nullable=False
    )

    started_at: Mapped[datetime] = mapped_column(index=True)
    finished_at: Mapped[datetime | None]
    total_area_m2: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        comment="Area this activity covers (validate against field area)"
    )

    notes: Mapped[str | None]
    status: Mapped[ActivityStatus] = mapped_column(
        default=ActivityStatus.PLANNED, nullable=False
    )

    # Relationships
    creator: Mapped['User'] = relationship(
        back_populates='created_activities', init=False
    )
    field: Mapped['Field'] = relationship(
        back_populates='activities', init=False
    )

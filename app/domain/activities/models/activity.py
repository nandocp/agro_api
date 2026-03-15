from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import CheckConstraint, Date, ForeignKey, Numeric, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.activities.enums import ActivityStatus
from app.shared.model import BaseModel

if TYPE_CHECKING:
    from app.domain.accounts.models import User
    from app.domain.fields.models import Field


class Activity(BaseModel):
    __tablename__ = 'activities'
    __table_args__ = (
        CheckConstraint('finished_at IS NULL OR finished_at >= started_at'),
        CheckConstraint(
            'total_area_m2 IS NULL OR total_area_m2 > 0',
            name='ck_activity_area_positive',
        ),
    )
    __mapper_args__ = {
        'polymorphic_identity': 'activity',
        # discriminator: value that indicates object type
        'polymorphic_on': 'activity_type',
    }

    activity_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment='Polymorphic discriminator: planting, grazing, processing...',
    )

    field_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey('fields.id', ondelete='CASCADE'),
        index=True,
        nullable=False,
    )
    creator_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey('users.id', ondelete='RESTRICT'), nullable=False
    )

    kind = Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=None,
        comment='ActivityKind enum — validated by API layer',
    )

    started_at: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    finished_at: Mapped[date | None] = mapped_column(
        Date, nullable=True, default=None
    )
    total_area_m2: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
        default=None,
        comment='Area this activity covers (validate against field area)',
    )

    status: Mapped[str] = mapped_column(
        String(64), default=ActivityStatus.PLANNING.value, nullable=False
    )

    # Relationships
    creator: Mapped['User'] = relationship(
        'User', back_populates='created_activities', init=False
    )
    field: Mapped['Field'] = relationship(
        'Field', back_populates='activities', init=False
    )

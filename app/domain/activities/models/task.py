from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING, List
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    String,
    Text,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.activities.enums import TaskStatus
from app.shared.model import BaseModel

if TYPE_CHECKING:
    from app.domain.accounts.models import User
    from app.domain.activities.models import Activity


class ActivityTask(BaseModel):
    __tablename__ = 'activity_tasks'
    __table_args__ = (
        CheckConstraint(
            (
                'completed_at IS NULL '
                'OR started_at IS NULL '
                'OR completed_at >= started_at'
            ),
            name='ck_task_completed_after_started',
        ),
        CheckConstraint(
            'parent_task_id != id',
            name='ck_task_no_self_reference',
        ),
    )

    activity_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey('activities.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )
    creator_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey('users.id', ondelete='RESTRICT'), nullable=False
    )
    assigned_to_id: Mapped[UUID | None] = mapped_column(
        Uuid, ForeignKey('users.id', ondelete='SET NULL'), nullable=True
    )

    title: Mapped[str | None] = mapped_column(
        String(200), nullable=True, default=None
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)

    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default=TaskStatus.PENDING.value
    )
    priority: Mapped[str | None] = mapped_column(
        String(50), nullable=True, default=None
    )

    due_date: Mapped[date | None] = mapped_column(
        Date, nullable=True, default=None
    )
    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None, nullable=True
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None, nullable=True
    )

    parent_task_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey('activity_tasks.id', ondelete='SET NULL'),
        nullable=True,
        default=None,
    )

    activity: Mapped['Activity'] = relationship(
        back_populates='tasks', init=False, lazy='raise'
    )
    creator: Mapped['User'] = relationship(
        foreign_keys=[creator_id], init=False, lazy='raise'
    )
    assigned_to: Mapped['User | None'] = relationship(
        foreign_keys=[assigned_to_id], init=False, lazy='raise'
    )
    parent_task: Mapped['ActivityTask'] = relationship(
        foreign_keys=[parent_task_id],
        remote_side='ActivityTask.id',
        back_populates='subtasks',
        lazy='raise',
        init=False,
    )
    subtasks: Mapped[List['ActivityTask']] = relationship(
        back_populates='parent_task',
        cascade='all, delete-orphan',
        init=False,
        lazy='raise',
    )

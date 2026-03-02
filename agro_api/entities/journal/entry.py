from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List

from geoalchemy2 import Geometry
from sqlalchemy import (
    ForeignKey,
    String,
    Text,
    Uuid,
    func
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
    from agro_api.entities.task import Task


@mapped_as_dataclass(table_registry, kw_only=True)
class JournalEntry(BaseEntity):
    """A narrative entry in an activity's journal."""
    __tablename__ = 'journal_entries'

    author_id: Mapped[Uuid] = mapped_column(
        ForeignKey('users.id', ondelete='RESTRICT'),
        nullable=False,
        index=True
    )

    logged_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
        index=True
    )

    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    is_pinned: Mapped[bool] = mapped_column(default=False)

    author: Mapped['User'] = relationship(foreign_keys=[author_id])

    # Tasks created from this entry
    created_tasks: Mapped[List['Task']] = relationship(
        back_populates='source_journal_entry',
        init=False
    )

    def __repr__(self):
        return f"JournalEntry(id={self.id}, title={self.title[:19]}, date={self.logged_at.date()})"

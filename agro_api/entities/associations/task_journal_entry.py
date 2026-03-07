from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
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
    from agro_api.entities.journal import JournalEntry
    from agro_api.entities.task import Task


@mapped_as_dataclass(table_registry, kw_only=True)
class TaskJournalEntry(BaseEntity):
    """A note or update entry specifically attached to a task."""
    __tablename__ = 'task_journal_entries'

    task_id: Mapped[Uuid] = mapped_column(
        ForeignKey('tasks.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    author_id: Mapped[Uuid] = mapped_column(
        ForeignKey('users.id', ondelete='RESTRICT'),
        nullable=False
    )

    # Optional link to the main journal entry that prompted this
    journal_entry_id: Mapped[Uuid | None] = mapped_column(
        ForeignKey('journal_entries.id', ondelete='SET NULL'),
        index=True,
        nullable=False
    )

    # Relationships
    task: Mapped['Task'] = relationship(
        back_populates='journal_entries', init=False
    )
    author: Mapped['User'] = relationship(lazy='joined', init=False)
    source_journal_entry: Mapped['JournalEntry'] = relationship(
        foreign_keys=[journal_entry_id],
        init=False
    )

    def __repr__(self):
        return (
            f"TaskJournalEntry("
            f"id={self.id}, "
            f"task={self.task_id}, "
            f"journal_entry={self.journal_entry_id}"
            ")"
        )

from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.model import BaseModel

if TYPE_CHECKING:
    from app.domain.accounts.models import User


class JournalEntry(BaseModel):
    """A narrative entry in an entity's journal."""

    __tablename__ = 'journal_entries'
    __table_args__ = (
        Index('ix_journal_entry_entity', 'entity_type', 'entity_id'),
        CheckConstraint(
            'length(trim(content)) > 0',
            name='ck_journal_entry_content_not_empty',
        ),
    )

    entity_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment='Validated by API layer',
    )
    entity_id: Mapped[UUID] = mapped_column(
        Uuid,
        nullable=False,
        index=True,
    )
    author_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey('users.id', ondelete='RESTRICT'),
        nullable=False,
        index=True,
    )

    logged_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )

    title: Mapped[str | None] = mapped_column(
        String(200), nullable=True, default=None
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_pinned: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, init=False
    )

    author: Mapped['User'] = relationship(
        'User', foreign_keys=[author_id], lazy='raise', init=False
    )

    def __repr__(self):
        return (
            f'JournalEntry('
            f'id={self.id}, '
            f'entity={self.entity_type}, '
            f'title={self.title[:19].strip()}, '
            f'date={self.logged_at.date()}'
            ')'
        )

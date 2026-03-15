from __future__ import annotations

from sqlalchemy import ForeignKey, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.model import BaseModel


class OrganismSynonym(BaseModel):
    __tablename__ = 'organism_synonyms'
    __table_args__ = (
        UniqueConstraint('organism_id', 'value', name='uq_organism_synonym'),
    )

    organism_id: Mapped[Uuid] = mapped_column(
        ForeignKey('organisms.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )

    value: Mapped[str] = mapped_column(String(200), nullable=False)
    authorship: Mapped[str | None] = mapped_column(
        String(200), nullable=True, default=None
    )

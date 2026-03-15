from __future__ import annotations

from sqlalchemy import ForeignKey, String, UniqueConstraint, Uuid
from sqlalchemy.dialects.postgresql import JSONB
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

    scientific_name: Mapped[str] = mapped_column(String(200), nullable=False)
    taxonomy: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
        default=None,
        comment='Full taxonomic classification previous to current one',
    )
    authorship: Mapped[str | None] = mapped_column(
        String(200), nullable=True, default=None
    )

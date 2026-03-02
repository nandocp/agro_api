from __future__ import annotations

from sqlalchemy import ForeignKey, Index, String, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
)

from agro_api.entities.base import BaseEntity
from config.database import table_registry


@mapped_as_dataclass(table_registry)
class PlantSynonym(BaseEntity):
    """Scientific names that are no longer accepted."""
    __tablename__ = 'plant_synonyms'
    __table_args__ = (
        Index('idx_synonym_search', 'synonym_name'),
    )

    accepted_id: Mapped[Uuid] = mapped_column(ForeignKey('plant_species.id'))

    synonym_name: Mapped[str] = mapped_column(
        String(200),
        unique=True,  # Each synonym is unique
        index=True
    )
    # authorship: Mapped[str | None]

    # Reference for the synonymy
    # reference: Mapped[str | None]  # e.g., "Flora do Brasil 2020"

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Index, String, UniqueConstraint, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
)

from config.database import table_registry


@mapped_as_dataclass(table_registry)
class PlantCommonName():
    __tablename__ = 'plant_common_names'
    __table_args__ = (
        UniqueConstraint('species_id', 'name', 'language', name='uq_species_name_lang'),
        Index('idx_common_name_search', 'name'),  # For text search
    )

    id: Mapped[Uuid] = mapped_column(primary_key=True)
    species_id: Mapped[Uuid] = mapped_column(ForeignKey('plant_species.id'))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    region: Mapped[str | None]
    language: Mapped[str] = mapped_column(String(10), default='pt-BR')
    is_preferred: Mapped[bool] = mapped_column(
        default=False,
        comment='Preferred name for display in this language/region'
    )

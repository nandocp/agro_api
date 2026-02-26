from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List

from sqlalchemy import String, UniqueConstraint, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
)

from agro_api.entities.plant import (
    PlantCycle,
    GrowthHabit,
    PlantUse,
    WaterRequirement
)
from config.database import table_registry

if TYPE_CHECKING:
    from agro_api.entities.plant import PlantCommonName, PlantSynonym


@mapped_as_dataclass(table_registry)
class PlantSpecies():
    __tablename__ = 'plant_species'
    __table_args__ = (
        UniqueConstraint('scientific_name', name='idx_scientific_name')
    )

    id: Mapped[Uuid] = mapped_column(
        UUID,
        init=False,
        primary_key=True,
        server_default=func.uuidv7(),
        nullable=False,
    )

    # Identification
    scientific_name: Mapped[str] = mapped_column(
        String(200),
        unique=True,
        nullable=False,
        index=True
    )

    # Classification
    plant_cycle: Mapped[PlantCycle]
    growth_habit: Mapped[GrowthHabit]

    # Use categories (can be multiple)
    primary_use: Mapped[PlantUse]
    secondary_uses: Mapped[List[PlantUse] | None] = mapped_column()

    # Characteristics
    max_height_m: Mapped[float | None]
    min_temperature_c: Mapped[float | None]
    max_temperature_c: Mapped[float | None]
    water_requirement: Mapped[WaterRequirement | None]  # low, medium, high

    # Common names
    common_names: Mapped[List['PlantCommonName']] = relationship(
        cascade='all, delete-orphan',
        lazy='selectin'
    )

    # Scientific synonyms (names that are no longer accepted)
    synonyms: Mapped[List['PlantSynonym']] = relationship(
        cascade='all, delete-orphan',
        lazy='selectin'
    )

    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

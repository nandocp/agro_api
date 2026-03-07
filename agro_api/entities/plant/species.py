from __future__ import annotations

from typing import TYPE_CHECKING, List

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
)

from agro_api.entities.base import BaseEntity
from agro_api.entities.plant import (
    GrowthHabit,
    PlantCycle,
    PlantUse,
    WaterRequirement,
)
from config.database import table_registry

if TYPE_CHECKING:
    from agro_api.entities.plant import PlantCommonName, PlantSynonym


@mapped_as_dataclass(table_registry)
class PlantSpecies(BaseEntity):
    __tablename__ = 'plant_species'
    __table_args__ = (
        UniqueConstraint('scientific_name', name='idx_scientific_name')
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

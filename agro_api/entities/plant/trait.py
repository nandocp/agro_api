from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
)

from agro_api.entities.base import BaseEntity
from agro_api.entities.plant import TraitCategory
from config.database import table_registry


@mapped_as_dataclass(table_registry)
class PlantTrait(BaseEntity):
    __tablename__ = 'plant_traits'

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,  # No duplicate trait names
        nullable=False
    )
    category: Mapped[TraitCategory] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column(String(500))

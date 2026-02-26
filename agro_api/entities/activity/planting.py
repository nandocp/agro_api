from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Numeric,
    String,
    Uuid,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
)

from agro_api.entities.activity import (
    Activity,
    PlantingArrangement,
    PlantingPurpose,
    PlantingStratum,
)
from config.database import table_registry

if TYPE_CHECKING:
    from agro_api.entities.plant import PlantSpecies


@mapped_as_dataclass(table_registry, kw_only=True)
class Planting(Activity):
    __tablename__ = 'plantings'
    __mapper_args__ = {'polymorphic_identity': 'planting'}
    __table_args__ = (
        CheckConstraint('density_per_ha > 0'),
        CheckConstraint('row_spacing_cm IS NULL OR row_spacing_cm > 0'),
        CheckConstraint('plant_spacing_cm IS NULL OR plant_spacing_cm > 0'),
    )

    id: Mapped[Uuid] = mapped_column(
        UUID,
        ForeignKey("activities.id"),
        primary_key=True,
        init=False
    )

    # What was planted
    plant_species_id: Mapped[Uuid] = mapped_column(
        ForeignKey('plant_species.id'), nullable=False
    )
    variety: Mapped[str | None] = mapped_column(String(64))

    # How it was planted
    spatial_arrangement: Mapped[PlantingArrangement]
    row_spacing_cm: Mapped[float | None]
    plant_spacing_cm: Mapped[float | None]
    density_per_ha: Mapped[int]

    # Which stratum the plant occupies
    stratum: Mapped[PlantingStratum | None]

    # Commercial info
    primary_purpose: Mapped[PlantingPurpose]
    is_commodity: Mapped[bool] = mapped_column(
        default=False,
        comment="True for commodity crops (soy, corn), False for specialty crops"
    )

    # Expected products
    expected_yield_kg_ha: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    actual_yield_kg_ha: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))

    # Relationships
    plant_species: Mapped[PlantSpecies] = relationship(init=False)

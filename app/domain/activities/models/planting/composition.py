from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, List

from app.entities.activity.planting import (
    GeneticSource,
    PlantingPurpose,
    PlantingStratum,
)
from app.entities.base import BaseEntity
from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from agro_api.
from config.database import table_registry

if TYPE_CHECKING:
    from app.entities.activity.planting import Planting
    from app.entities.associations import PlantingCompositionTrait
    from app.entities.plant import PlantSpecies


@table_registry.mapped_as_dataclass(kw_only=True)
class PlantingComposition(BaseEntity):
    __tablename__ = 'planting_compositions'
    __table_args__ = (
        CheckConstraint(
            'proportion >= 0 AND proportion <= 1', name='ck_proportion_range'
        ),
        CheckConstraint('density_per_ha > 0', name='ck_density_positive'),
    )

    planting_id: Mapped[Uuid] = mapped_column(
        ForeignKey('plantings.id', ondelete='CASCADE'), primary_key=True
    )
    plant_species_id: Mapped[Uuid] = mapped_column(
        ForeignKey('plant_species.id', ondelete='RESTRICT'), primary_key=True
    )
    cultivar_name: Mapped[str | None] = mapped_column(
        String(64), index=True, comment='Cabernet sauvignon, Criolo Roxo, etc.'
    )

    # Commercial info
    primary_purpose: Mapped[PlantingPurpose]
    is_commodity: Mapped[bool] = mapped_column(
        default=False,
        comment='Commodities are traded globally; specialties are niche.',
    )
    expected_yield_kg_per_ha: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2)
    )

    # Proporção da espécie na área total do plantio (0.0 a 1.0)
    proportion: Mapped[Decimal] = mapped_column(Numeric(3, 2), nullable=False)
    density_per_ha: Mapped[int]
    stratum: Mapped[PlantingStratum | None] = mapped_column(
        comment='Which stratum the plant occupies'
    )
    genetic_source: Mapped[GeneticSource] = mapped_column(
        default=GeneticSource.UNKNOWN,
        comment='Where the genetic material came from.',
    )

    planting: Mapped['Planting'] = relationship(back_populates='composition')
    plant_species: Mapped['PlantSpecies'] = relationship(lazy='joined')
    traits: Mapped[List['PlantingCompositionTrait']] = relationship(
        back_populates='planting', cascade='all, delete-orphan', init=False
    )

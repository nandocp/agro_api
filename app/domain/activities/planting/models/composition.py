from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, List
from uuid import UUID

from sqlalchemy import (
    ARRAY,
    Boolean,
    CheckConstraint,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.activities.planting.enums import PlantingGeneticSource
from app.shared.model import BaseModel

if TYPE_CHECKING:
    from app.domain.activities.models import Planting, PlantingCompositionTrait
    from app.domain.organisms.models import Organism


class PlantingComposition(BaseModel):
    __tablename__ = 'planting_compositions'
    __table_args__ = (
        CheckConstraint(
            'proportion >= 0 AND proportion <= 1', name='ck_proportion_range'
        ),
        CheckConstraint('density_per_ha > 0', name='ck_density_positive'),
        UniqueConstraint(
            'planting_id',
            'plant_species_id',
            'cultivar_name',
            name='uq_planting_composition_species_cultivar',
        ),
    )

    planting_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey('plantings.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )
    plant_species_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey('organisms.id', ondelete='RESTRICT'), nullable=False
    )
    cultivar_name: Mapped[str | None] = mapped_column(
        String(128),
        comment='Cabernet sauvignon, Criolo Roxo, etc.',
        nullable=True,
        default=None,
    )
    # Commercial info
    primary_purpose: Mapped[str | None] = mapped_column(
        String(50),
        default=None,
        nullable=True,
        comment='PlantingPurpose enum. Validated by API layer',
    )
    secondary_purposes: Mapped[List[str] | None] = mapped_column(
        ARRAY(String(50)),
        nullable=True,
        default=None,
        comment='PlantingPurpose enum. Validated by API layer',
    )
    is_commodity: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment='Commodities are traded globally; specialties are niche.',
    )
    expected_yield_kg_per_ha: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2), default=None, nullable=True
    )

    # Proporção da espécie na área total do plantio (0.0 a 1.0)
    proportion: Mapped[Decimal | None] = mapped_column(
        Numeric(4, 2), nullable=True, default=None
    )
    density_per_ha: Mapped[int | None] = mapped_column(
        Integer, nullable=True, default=None
    )
    stratum: Mapped[str | None] = mapped_column(
        String(50),
        default=None,
        nullable=True,
        comment='Which stratum the plant occupies',
    )
    genetic_source: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        default=PlantingGeneticSource.UNKNOWN.value,
        comment='Where the genetic material came from.',
    )

    planting: Mapped['Planting'] = relationship(
        'Planting', back_populates='composition', lazy='raise', init=False
    )
    plant_species: Mapped['Organism'] = relationship(
        'Organism', lazy='raise', init=False
    )
    traits: Mapped[List['PlantingCompositionTrait']] = relationship(
        'PlantingCompositionTrait',
        back_populates='planting',
        cascade='all, delete-orphan',
        init=False,
        lazy='raise',
    )

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    String,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
)

from agro_api.entities.base import BaseEntity
from config.database import table_registry

if TYPE_CHECKING:
    from agro_api.entities.activity import Planting
    from agro_api.entities.plant import PlantTrait


@mapped_as_dataclass(table_registry, kw_only=True)
class PlantingTrait(BaseEntity):
    __tablename__ = 'planting_traits'
    __table_args__ = (
        UniqueConstraint(
            'planting_id', 'plant_trait_id', name='uq_planting_trait'
        ),
    )

    planting_id: Mapped[Uuid] = mapped_column(
        ForeignKey('plantings.id', ondelete='CASCADE'),
        primary_key=True
    )
    plant_trait_id: Mapped[Uuid] = mapped_column(
        ForeignKey('plant_traits.id', ondelete='RESTRICT'),
        primary_key=True
    )
    value: Mapped[str | None] = mapped_column(
        String(32),
        comment="For quantitative traits: '85%', 'RR1', etc."
    )

    # Relationships
    planting: Mapped['Planting'] = relationship(
        back_populates='traits', init=False
    )
    trait: Mapped['PlantTrait'] = relationship(
        foreign_keys=[plant_trait_id], init=False
    )

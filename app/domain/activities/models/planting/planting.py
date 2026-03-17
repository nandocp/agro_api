"""
São utilizados três conceitos fundamentais para representar
a diversidade de sistemas agrícolas: estrutura de plantio,
composição de espécies e padrão de repetição.
Cada um deles é capturado por diferentes partes do modelo,
e a combinação deles permite descrever desde uma monocultura simples
até sistemas agroflorestais complexos. Vamos
"""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from app.entities.activity import Activity
from sqlalchemy import ForeignKey, Uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
)

from config.database import table_registry

if TYPE_CHECKING:
    from app.entities.activity.planting import PlantingComposition


@mapped_as_dataclass(table_registry, kw_only=True)
class Planting(Activity):
    __tablename__ = 'plantings'
    __mapper_args__ = {'polymorphic_identity': 'planting'}

    id: Mapped[Uuid] = mapped_column(
        UUID, ForeignKey('activities.id'), primary_key=True, init=False
    )

    composition: Mapped[List['PlantingComposition']] = relationship(
        back_populates='planting', cascade='all, delete-orphan', init=False
    )

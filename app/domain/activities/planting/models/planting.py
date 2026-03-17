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
from uuid import UUID

from sqlalchemy import ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.activities.models import Activity

if TYPE_CHECKING:
    from app.domain.activities.models import PlantingComposition


class Planting(Activity):
    __tablename__ = 'plantings'
    __mapper_args__ = {'polymorphic_identity': 'planting'}

    id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey('activities.id'),
        primary_key=True,
        init=False,
        nullable=False,
    )

    composition: Mapped[List['PlantingComposition']] = relationship(
        'PlantingComposition',
        back_populates='planting',
        cascade='all, delete-orphan',
        init=False,
    )

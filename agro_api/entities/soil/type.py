from __future__ import annotations

from typing import List

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

[
    'Argissolos',
    'Cambissolos',
    'Chernossolos',
    'Espodossolos',
    'Gleissolos',
    'Latossolos',
    'Luvissolos',
    'Neossolos',
    'Nitossolos',
    'Organossolos',
    'Planossolos',
    'Plintossolos',
    'Vertissolos'
]


@mapped_as_dataclass(table_registry, kw_only=True)
class SoilType(BaseEntity):
    """Lookup table for soil types from various classification systems."""
    __tablename__ = 'soil_types'
    __table_args__ = (
        UniqueConstraint('name', 'source', name='uq_soil_name_source'),
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Soil type name, e.g., 'Latossolos', 'Chernozem'"
    )
    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Classification system, e.g., 'SiBCS', 'WRB'"
    )

    # Optional: hierarchical relationship (for systems with multiple levels)
    parent_id: Mapped[Uuid | None] = mapped_column(
        ForeignKey('soil_types.id', ondelete='SET NULL'),
        comment="""
        For hierarchical systems: parent soil type
        (e.g., order → suborder)
        """
    )
    parent: Mapped['SoilType'] = relationship(
        remote_side='SoilType.id',
        back_populates='children',
        init=False
    )
    children: Mapped[List['SoilType']] = relationship(
        back_populates='parent',
        cascade='all, delete-orphan',
        init=False
    )

    def __repr__(self):
        return f"SoilType(name={self.name}, source={self.source})"

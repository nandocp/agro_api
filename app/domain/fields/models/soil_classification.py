from __future__ import annotations

from typing import List
from uuid import UUID

from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Table,
    Text,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.model import BaseModel, DeclarativeModel


class SoilClassification(BaseModel):
    """Lookup table for soil types from various classification systems."""

    __tablename__ = 'soil_classifications'
    __table_args__ = (
        UniqueConstraint('name', 'source', name='uq_soil_name_source'),
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Soil type name, e.g., 'Latossolos', 'Chernozem'",
    )
    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Classification system, e.g., 'SiBCS', 'WRB'",
    )
    description: Mapped[str | None] = mapped_column(
        Text, nullable=True, default=None
    )

    # Optional: hierarchical relationship (for systems with multiple levels)
    parent_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey('soil_classifications.id', ondelete='SET NULL'),
        comment="""
        For hierarchical systems: parent soil type
        (e.g., order → suborder)
        """,
        default=None,
        nullable=True,
    )
    parent: Mapped['SoilClassification | None'] = relationship(
        'SoilClassification',
        foreign_keys=[parent_id],
        remote_side='SoilClassification.id',
        back_populates='children',
        init=False,
        lazy='raise',
    )
    children: Mapped[List['SoilClassification']] = relationship(
        'SoilClassification',
        back_populates='parent',
        cascade='all, delete-orphan',
        init=False,
        lazy='raise',
    )

    def __repr__(self):
        return f'SoilClassification(name={self.name}, source={self.source})'


FieldSoilClassification = Table(
    'field_soil_classifications',
    DeclarativeModel.metadata,
    Column(
        'field_id',
        ForeignKey('fields.id', ondelete='CASCADE'),
        primary_key=True,
    ),
    Column(
        'soil_classification_id',
        ForeignKey('soil_classifications.id', ondelete='RESTRICT'),
        primary_key=True,
    ),
)

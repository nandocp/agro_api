from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
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
    from agro_api.entities.field import Field
    from agro_api.entities.soil import SoilClassification


@mapped_as_dataclass(table_registry, kw_only=True)
class FieldSoilClassification(BaseEntity):
    __tablename__ = 'field_soil_classifications'
    __table_args__ = (
        UniqueConstraint(
            'field_id',
            'soil_classification_id',
            name='uq_field_soil_classification',
        ),
    )

    field_id: Mapped[Uuid] = mapped_column(
        ForeignKey('fields.id', ondelete='CASCADE'), primary_key=True
    )
    soil_classification_id: Mapped[Uuid] = mapped_column(
        ForeignKey('soil_classifications.id', ondelete='RESTRICT'),
        primary_key=True,
    )

    # Relationships
    field: Mapped['Field'] = relationship(foreign_keys=field_id, init=False)
    soil_classification: Mapped['SoilClassification'] = relationship(
        foreign_keys=[soil_classification_id], init=False
    )

from uuid import UUID

from sqlalchemy import Boolean, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ..organism import Organism


class Animal(Organism):
    __tablename__ = 'animals'
    __mapper_args__ = {'polymorphic_identity': 'animal'}

    organism_id: Mapped[UUID] = mapped_column(
        ForeignKey('organisms.id'), primary_key=True, init=False
    )
    animal_class: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        default=None,
        comment='mammalia, aves, insecta, arachnida...',
    )
    avg_weight_kg: Mapped[float | None] = mapped_column(
        Float, nullable=True, default=None
    )
    is_domestic: Mapped[bool | None] = mapped_column(
        Boolean, nullable=True, default=None
    )

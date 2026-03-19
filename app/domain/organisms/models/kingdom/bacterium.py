from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ..organism import Organism


class Bacterium(Organism):
    __tablename__ = 'bacteria'
    __mapper_args__ = {'polymorphic_identity': 'bacterium'}

    organism_id: Mapped[UUID] = mapped_column(
        ForeignKey('organisms.id'), primary_key=True, init=False
    )
    strain: Mapped[str | None] = mapped_column(
        String(100), nullable=True, default=None
    )
    bacterium_use: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        default=None,
        comment='inoculant, biocontrol, biofertilizer...',
    )

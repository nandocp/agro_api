from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ..organism import Organism


class Fungus(Organism):
    __tablename__ = 'fungi'
    __mapper_args__ = {'polymorphic_identity': 'fungus'}

    organism_id: Mapped[UUID] = mapped_column(
        ForeignKey('organisms.id'), primary_key=True, init=False
    )
    fungus_use: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        default=None,
        comment='inoculant, food, biocontrol...',
    )

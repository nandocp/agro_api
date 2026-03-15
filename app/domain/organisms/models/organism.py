from typing import TYPE_CHECKING, List

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.model import BaseModel

if TYPE_CHECKING:
    from app.domain.organisms.models import OrganismCommonName, OrganismSynonym


class Organism(BaseModel):
    __tablename__ = 'organisms'
    __table_args__ = (
        UniqueConstraint(
            'scientific_name', name='uq_organism_scientific_name'
        ),
    )
    __mapper_args__ = {
        'polymorphic_identity': 'organism',
        'polymorphic_on': 'organism_type',
    }

    organism_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment='Polymorphic discriminator: plant, animal, fungus, bacterium',
    )
    taxonomy: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
        default=None,
        comment='Full taxonomic classification',
    )
    scientific_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        index=True,
        comment='Binomial nomenclature: Genus species',
    )
    authorship: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
        default=None,
        comment='Taxonomic authority, who named the organism: e.g. (L.) Merr.',
    )
    external_ids: Mapped[dict | None] = mapped_column(
        JSONB,
        default=None,
        nullable=True,
        comment='External API identifiers',
    )

    common_names: Mapped[List['OrganismCommonName']] = relationship(
        cascade='all, delete-orphan', lazy='raise', init=False
    )
    synonyms: Mapped[List['OrganismSynonym']] = relationship(
        cascade='all, delete-orphan', lazy='raise', init=False
    )

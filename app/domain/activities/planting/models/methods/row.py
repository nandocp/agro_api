from __future__ import annotations

from typing import List

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Index,
    PrimaryKeyConstraint,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.model import BaseModel

from ..planting import Planting


class RowPlanting(Planting):
    __tablename__ = 'row_plantings'
    __mapper_args__ = {'polymorphic_identity': 'row_planting'}
    __table_args__ = (
        CheckConstraint('row_spacing_cm > 0'),
        CheckConstraint('total_rows > 0'),
    )

    id: Mapped[Uuid] = mapped_column(
        ForeignKey('plantings.id'), primary_key=True
    )

    row_spacing_cm: Mapped[float] = mapped_column(nullable=False)
    total_rows: Mapped[int]

    # Relacionamento com a definição detalhada de cada tipo de linha
    row_types: Mapped[List['RowType']] = relationship(
        back_populates='row_planting', cascade='all, delete-orphan', init=False
    )


# Defines a row type inside a Row Planting method
class RowType(BaseModel):
    __tablename__ = 'row_types'
    __table_args__ = (UniqueConstraint('row_planting_id', 'code'),)

    row_planting_id: Mapped[Uuid] = mapped_column(
        ForeignKey('row_plantings.id')
    )

    # Padrão de repetição de espécies DENTRO desta linha
    # Ex: para linha tipo 'A' com padrão [sp1, sp2, sp1, sp2] a cada 30cm
    row_type_elements: Mapped[List['RowTypeElement']] = relationship(
        cascade='all, delete-orphan'
    )
    order: Mapped[RowTypeOrder] = relationship(init=False)


class RowTypeOrder(BaseModel):
    __tablename__ = 'row_type_orders'
    __table_args__ = (
        PrimaryKeyConstraint(
            'row_planting_id', 'position', name='pk_row_planting_type_order'
        ),
        Index('ix_row_planting_type_order_type', 'row_type_id'),
    )

    position: Mapped[int] = mapped_column(
        nullable=False,
        comment='Ordem do tipo de linha na sequência (0,1,2...)',
    )
    row_type_id: Mapped[Uuid] = mapped_column(
        ForeignKey('row_types.id', ondelete='RESTRICT'), nullable=False
    )


# Defines an element in the repetition pattern inside a row
class RowTypeElement(BaseModel):
    __tablename__ = 'row_type_elements'

    row_type_id: Mapped[Uuid] = mapped_column(ForeignKey('row_types.id'))
    planting_composition_id: Mapped[Uuid] = mapped_column(
        ForeignKey('planting_compositions.id')
    )
    sequence_position: Mapped[int]  # 1º, 2º, 3º elemento do padrão
    distance_to_next_cm: Mapped[float] = mapped_column(
        comment='Distância para o próximo elemento na sequência.'
    )

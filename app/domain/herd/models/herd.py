class Herd(ModelBase):
    __tablename__ = 'herds'

    estate_id: Mapped[UUID] = mapped_column(
        ForeignKey('estates.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )
    organism_id: Mapped[UUID] = mapped_column(
        ForeignKey('organisms.id', ondelete='RESTRICT'),
        nullable=False,
        comment='Animal species — must be kingdom=animalia',
    )
    name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        default=None,
        comment='Optional herd name — e.g. Lote A, Rebanho Nelore',
    )
    total_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment='Total number of animals in herd',
    )
    unit: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment='HerdUnit enum — head, hive, tank, flock, colony',
    )
    is_individualized: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        comment='True if herd has individual animal records',
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=HerdStatus.ACTIVE.value,
    )
    notes: Mapped[str | None] = mapped_column(
        Text, nullable=True, default=None
    )

    estate: Mapped['Estate'] = relationship(
        back_populates='herds', lazy='raise', init=False
    )
    species: Mapped['Organism'] = relationship(lazy='raise', init=False)
    animals: Mapped[list['HerdAnimal']] = relationship(
        back_populates='herd',
        cascade='all, delete-orphan',
        lazy='raise',
        init=False,
    )

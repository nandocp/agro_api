class Address:
    __tablename__ = 'addresses'

    id: Mapped[Uuid] = mapped_column(primary_key=True, server_default=func.uuidv7())

    # Core address fields
    street: Mapped[str | None]
    number: Mapped[str | None]  # String to handle "S/N", "Km 12", etc.
    complement: Mapped[str | None]
    neighborhood: Mapped[str | None]
    city: Mapped[str]
    state: Mapped[str]  # Could be FK to states table
    postal_code: Mapped[str | None]
    country: Mapped[str] = mapped_column(default='BR')

    # Optional geocoding fields
    latitude: Mapped[float | None]
    longitude: Mapped[float | None]
    geocoding_accuracy: Mapped[str | None]  # rooftop, street, approximate, etc.

    # Metadata
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    estate: Mapped['Estate'] = relationship(back_populates='address')

-------------------------------------------------------------------------------------------------
PLOT: add soil_type

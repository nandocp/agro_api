class ActivityEvent(ORMBase):
    __tablename__ = 'activity_events'

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid4)
    activity_id: Mapped[UUID] = mapped_column(
        ForeignKey('activities.id'), nullable=False, index=True
    )
    document_id: Mapped[UUID | None] = mapped_column(
        ForeignKey('activity_documents.id'),
        nullable=True,
        comment='Populated when event is related to a document',
    )
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
    previous_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    current_hash: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    created_by: Mapped[UUID] = mapped_column(
        ForeignKey('users.id'), nullable=False
    )

    activity: Mapped['Activity'] = relationship(lazy='raise', init=False)
    document: Mapped['ActivityDocument | None'] = relationship(
        lazy='raise', init=False
    )

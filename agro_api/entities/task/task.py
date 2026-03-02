
@mapped_as_dataclass(table_registry, kw_only=True)
class Task(BaseEntity):
    __tablename__ = 'tasks'

    activity_id: Mapped[Uuid] = mapped_column(
        ForeignKey('activities.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    creator_id: Mapped[Uuid] = mapped_column(
        ForeignKey('users.id', ondelete='RESTRICT'),
        nullable=False
    )
    assigned_to_id: Mapped[Uuid | None] = mapped_column(
        ForeignKey('users.id', ondelete='SET NULL'),
        index=True
    )

    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)

    status: Mapped[TaskStatus]
    priority: Mapped[TaskPriority]

    due_date: Mapped[date | None] = mapped_column(index=True)
    started_at: Mapped[datetime | None]
    completed_at: Mapped[datetime | None]

    parent_task_id: Mapped[Uuid | None] = mapped_column(
        ForeignKey('tasks.id', ondelete='CASCADE'),
        index=True
    )

    # Relationships
    activity: Mapped['Activity'] = relationship(back_populates='tasks', init=False)
    creator: Mapped['User'] = relationship(foreign_keys=[creator_id], init=False)
    assigned_to: Mapped['User'] = relationship(foreign_keys=[assigned_to_id], init=False)
    parent_task: Mapped['Task'] = relationship(
        remote_side='Task.id',
        back_populates='subtasks',
        init=False
    )
    subtasks: Mapped[List['Task']] = relationship(
        back_populates='parent_task',
        cascade='all, delete-orphan',
        init=False
    )

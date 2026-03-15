from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from .declarative import DeclarativeModel


class BaseModel(DeclarativeModel):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        server_default=func.uuidv7(),
        init=False,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), init=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        init=False,
    )

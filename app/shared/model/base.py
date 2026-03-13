from datetime import datetime

from sqlalchemy import Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from .declarative import DeclarativeModel


class BaseModel(DeclarativeModel):
    __abstract__ = True

    id: Mapped[Uuid] = mapped_column(
        UUID,
        primary_key=True,
        server_default=func.uuidv7(),
        init=False,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), init=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), init=False
    )

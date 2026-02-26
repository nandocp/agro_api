from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

"""Base class for all entities with common fields."""
class BaseEntity:
    id: Mapped[UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=func.uuidv7(),
        init=False
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        init=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        init=False
    )

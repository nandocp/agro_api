import json
from datetime import datetime
from hashlib import sha256
from uuid import UUID

from app.domain.activities.models.event import ActivityEvent
from app.shared.events import DomainEvent
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class EventBus:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def publish(self, event: DomainEvent) -> ActivityEvent:
        previous_hash = await self._get_previous_hash(event.activity_id)
        hash_value = self._compute_hash(
            previous_hash,
            event.payload,
            event.occurred_at,
        )

        record = ActivityEvent(
            id=event.id,
            activity_id=event.activity_id,
            event_type=event.event_type,
            payload=event.payload,
            previous_hash=previous_hash,
            hash=hash_value,
            created_at=event.occurred_at,
            created_by=event.created_by,
        )
        self._session.add(record)
        await self._session.flush()
        return record

    async def _get_previous_hash(self, activity_id: UUID) -> str:
        result = await self._session.scalar(
            select(ActivityEvent.hash)
            .where(ActivityEvent.activity_id == activity_id)
            .order_by(ActivityEvent.created_at.desc())
            .limit(1)
        )
        return result or '0' * 64

    @staticmethod
    def _compute_hash(
        previous_hash: str,
        payload: dict,
        timestamp: datetime,
    ) -> str:
        content = (
            f'{previous_hash}'
            f'{json.dumps(payload, sort_keys=True)}'
            f'{timestamp.isoformat()}'
        )
        return sha256(content.encode()).hexdigest()

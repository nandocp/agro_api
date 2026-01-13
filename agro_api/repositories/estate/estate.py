from sqlalchemy import select

from agro_api.entities.estate import Estate
from agro_api.repositories.base import BaseRepository


class EstateRepository(BaseRepository):
    async def find_by_id(self, id: str) -> Estate | None:
        return await self.session.scalar(select(Estate).where(Estate.id == id))

    async def find_by(self, params: dict) -> Estate | None:
        stmt = select(Estate)

        for col, val in params.items():
            stmt = stmt.where(getattr(Estate, col) == val)

        return await self.session.scalar(stmt)

    async def query(self, filters, user_id):
        query = select(Estate).where(Estate.user_id == user_id)

        if filters.kind:
            query = query.filter(Estate.kind == filters.kind)

        if filters.label:
            query = query.filter(Estate.label.contains(filters.label))

        if filters.slug:
            query = query.filter(Estate.slug == filters.slug)

        return await self.session.scalars(query)

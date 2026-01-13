from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from agro_api.entities.estate import Estate
from agro_api.repositories.base import BaseRepository
from config.error_responses import unprocessable


class EstateRepository(BaseRepository):
    async def create(self, model):
        self.session.add(model)

        try:
            await self.session.commit()
            await self.session.refresh(model)

            return model
        except IntegrityError:
            unprocessable('Plot slug already exists')
        pass

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

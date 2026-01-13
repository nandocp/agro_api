from sqlalchemy import select

from agro_api.entities.estate import Estate
from agro_api.services.base import BaseService
from config.geometry import transform_point, transform_polygon


class EstateService(BaseService):
    def __init__(self, session=None, user=None):
        super().__init__(Estate, session, user)

    async def create(self, schema_params):
        new_estate = self.model(
            **schema_params.model_dump(),
            user_id=self.user.id
        )

        return await self.repository.create(new_estate)

    async def get_one(self, estate_id: str):
        filters = {'id': estate_id, 'user_id': self.user.id}
        return await self.repository.find_by(filters)
        # return await self.session.scalar(
        #     select(Estate)
        #     .where(Estate.id == estate_id)
        #     .where(Estate.user_id == self.user.id)
        # )

    async def get_many(self, filters):
        estates = await self.repository.query(filters, self.user.id)
        return {'estates': estates.all()}

    async def update(self, estate_id, params):
        estate = await self.session.scalar(
            select(Estate)
            .where(Estate.id == estate_id)
            .where(Estate.user_id == self.user.id)
        )

        if not estate:
            return False

        estate.slug = params.slug
        estate.label = params.label
        estate.kind = params.kind
        estate.opened_at = params.opened_at
        estate.closed_at = params.closed_at

        if params.coordinates:
            estate.coordinates = transform_point(params.coordinates)

        if params.limits:
            estate.limits = transform_polygon(params.limits)

        self.session.add(estate)
        await self.session.commit()
        await self.session.refresh(estate)

        return estate

    async def remove(self, *, id: int):
        pass

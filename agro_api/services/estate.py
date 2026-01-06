from geoalchemy2.shape import from_shape
from shapely.geometry import Point, Polygon
from sqlalchemy import select

from agro_api.entities.estate import Estate

from .base import BaseService


class EstateService(BaseService):
    def __init__(self, session=None, user=None):
        super().__init__(Estate, session, user)

    async def create(self, schema_params):
        new_estate = self.model(
            **schema_params.model_dump(),
            user_id=self.user.id
        )

        self.session.add(new_estate)
        await self.session.commit()
        await self.session.refresh(new_estate)

        return new_estate

    async def get_one(self, estate_id: str):
        return await self.session.scalar(
            select(Estate)
            .where(Estate.id == estate_id)
            .where(Estate.user_id == self.user.id)
        )

    async def get_many(self, filters):
        query = select(Estate).where(Estate.user_id == self.user.id)

        if filters.kind:
            query = query.filter(Estate.kind == filters.kind)

        if filters.label:
            query = query.filter(Estate.label.contains(filters.label))

        if filters.slug:
            query = query.filter(Estate.slug == filters.slug)

        estates = await self.session.scalars(query)
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
            estate.coordinates = EstateService.transform_coordinates(
                params.coordinates
            )

        if params.limits:
            estate.limits = EstateService.transform_limits(params.limits)

        self.session.add(estate)
        await self.session.commit()
        await self.session.refresh(estate)

        return estate

    async def remove(self, *, id: int):
        pass

    def transform_coordinates(raw_coordinates):
        if not raw_coordinates:
            return None

        coord_as_point = Point(raw_coordinates)
        return from_shape(coord_as_point, srid=4326)

    def transform_limits(raw_limits):
        if not raw_limits:
            return None

        limits_as_polygon = Polygon(raw_limits)
        return from_shape(limits_as_polygon, srid=4326)

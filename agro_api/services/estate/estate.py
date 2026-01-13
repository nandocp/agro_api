from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from agro_api.entities.estate import Estate
from agro_api.schemas.estate import EstateCreate, EstateFilter
from agro_api.services.base import BaseService
from config.authentication import validate_current_user
from config.http_misc import not_found, unprocessable


class EstateService(BaseService):
    async def create(self, schema_params: EstateCreate):
        validate_current_user(str(schema_params.user_id), str(self.user.id))

        try:
            return await self.repository.create(obj_in=schema_params)
        except IntegrityError:
            unprocessable('Estate.slug already exists')

    async def show(self, estate_id: str):
        filters = {'id': estate_id, 'user_id': self.user.id}
        estate = await self.repository.get_by(filters)
        if not estate:
            not_found()

        return estate

    async def index(self, filters: EstateFilter):
        new_filters = BaseService.extract_filters(filters)
        new_filters['user_id'] = self.user.id

        estates = await self.repository.get_many(
            new_filters, offset=filters.offset, limit=filters.limit
        )

        return {'estates': estates}

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

        self.session.add(estate)
        await self.session.commit()
        await self.session.refresh(estate)

        return estate

    async def remove(self, *, id: int):
        pass

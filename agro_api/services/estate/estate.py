from sqlalchemy.exc import IntegrityError

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
        estate = await self.repository.get_by({
            'id': estate_id, 'user_id': self.user.id
        })

        if not estate:
            not_found()

        try:
            return await self.repository.update(db_obj=estate, obj_in=params)
        except IntegrityError:
            unprocessable('Estate.slug already exists')

from agro_api.entities.estate import Estate
from agro_api.schemas.estate import EstateCreate, EstateFilter
from agro_api.services.estate import EstateService
from config.authentication import current_user
from config.database import session
from config.http_misc import filters


async def create_estate(
    session: session, user: current_user, params: EstateCreate
):
    args = {'model': Estate, 'session': session, 'current_user': user}
    return await EstateService(**args).create(params)


async def get_estates(
    session: session, user: current_user, filters: filters(EstateFilter)
):
    args = {'model': Estate, 'session': session, 'current_user': user}
    return await EstateService(**args).index(filters)

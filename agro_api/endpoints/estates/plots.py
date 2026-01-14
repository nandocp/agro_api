from agro_api.entities.estate import Plot
from agro_api.schemas.estate import PlotCreate, PlotFilter
from agro_api.services.estate import PlotService
from config.authentication import current_user
from config.database import session
from config.http_misc import filters


async def create_plot(
    session: session, user: current_user, estate_id: str, params: PlotCreate
):
    args = {'session': session, 'current_user': user, 'model': Plot}
    service = await PlotService(**args).create(params, estate_id)
    return service


async def show_plot(
    session: session, user: current_user, estate_id: str, id: str
):
    args = {'session': session, 'current_user': user, 'model': Plot}
    plot = await PlotService(**args).get_by_id(estate_id=estate_id, plot_id=id)
    return plot


async def index_plot(
    session: session,
    user: current_user,
    filters: filters(PlotFilter),
    estate_id: str
):
    args = {'session': session, 'current_user': user, 'model': Plot}
    plots = await PlotService(**args).get_list(filters, estate_id)
    return {'plots': plots}

from http import HTTPStatus

from fastapi import APIRouter

from agro_api.endpoints.estates import plots as plots_endpoints
from agro_api.schemas.common import BaseSchema
from agro_api.schemas.estate import PlotItem, PlotsList

router = APIRouter(prefix='/estates/{estate_id}/plots', tags=['estate_plots'])


router.add_api_route(
    '/',
    plots_endpoints.create_plot,
    methods=['POST'],
    response_model=BaseSchema,
    status_code=HTTPStatus.CREATED,
    summary='Create new Plot',
)


router.add_api_route(
    '/{id}',
    plots_endpoints.show_plot,
    methods=['GET'],
    response_model=PlotItem,
    status_code=HTTPStatus.OK,
    summary='Get Plot by id'
)


router.add_api_route(
    '/',
    plots_endpoints.index_plot,
    methods=['GET'],
    response_model=PlotsList,
    status_code=HTTPStatus.OK,
    summary='Get Plots list with pagination and filters'
)

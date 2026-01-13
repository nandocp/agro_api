from http import HTTPStatus

# from typing import Annotated
from fastapi import APIRouter  # , HTTPException, Query

from agro_api.schemas.estate_plot import (
    EstatePlotCreate,
    EstatePlotItem,
)
from agro_api.services.estate_plot import EstatePlotService
from config.database import session
from config.user import current_user

router = APIRouter(
    prefix='/estates/{estate_id}/estate_plots', tags=['estate_plots']
)
# filters = Annotated[EstateFilter, Query()]


@router.post(
    '/', response_model=EstatePlotItem, status_code=HTTPStatus.CREATED
)
async def create(
    session: session,
    user: current_user,
    plot: EstatePlotCreate,
    estate_id: str,
):
    return await EstatePlotService(session, user).create(plot, estate_id)

    # try:
    #     return service
    # except IntegrityError:
    #     raise HTTPException(
    #         status_code=HTTPStatus.UNPROCESSABLE_CONTENT,
    #         detail='Plot slug already exists',
    #     )

    # if not service:
    #     raise HTTPException(
    #         status_code=HTTPStatus.UNAUTHORIZED,
    #         detail='You shall not do it'
    #     )

    # if isinstance(service, str):
    #     raise HTTPException(
    #         status_code=HTTPStatus.UNPROCESSABLE_CONTENT,
    #         detail=service
    #     )

    # return service

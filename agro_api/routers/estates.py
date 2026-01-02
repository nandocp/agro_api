from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Query

from agro_api.schemas.estate import (
    EstateFilter,
    EstateGetResponseSchema,
    EstatePostPayloadSchema,
    EstatePostResponseSchema,
    EstatesList,
)
from agro_api.services.estate import EstateService
from config.database import session
from config.user import current_user

router = APIRouter(prefix='/estates', tags=['estates'])


@router.post('/',
    response_model=EstatePostResponseSchema,
    status_code=HTTPStatus.CREATED
)
def create(
    session: session,
    current_user: current_user,
    estate: EstatePostPayloadSchema
):
    return EstateService(session).create(estate, current_user.id)


@router.get('/', response_model=EstatesList, status_code=HTTPStatus.OK)
def index(
    session: session,
    current_user: current_user,
    filters: Annotated[EstateFilter, Query()]
):
    return EstateService(session).get_many(current_user.id, filters)


@router.get('/{estate_id}', response_model=EstateGetResponseSchema)
def show(session: session, current_user: current_user, estate_id: str):
    return EstateService(session).get_one(current_user.id, estate_id)

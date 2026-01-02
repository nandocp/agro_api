from http import HTTPStatus

from fastapi import APIRouter

from agro_api.schemas.estate import (
    EstatePostPayloadSchema,
    EstatePostResponseSchema,
)
from agro_api.services.estate import EstateService
from config.database import session
from config.user import current_user

router = APIRouter(prefix='/estates', tags=['estates'])


@router.post(
    '/',
    response_model=EstatePostResponseSchema,
    status_code=HTTPStatus.CREATED
)
def create(
    session: session,
    current_user: current_user,
    estate: EstatePostPayloadSchema
):
    return EstateService(session).create(estate, current_user.id)

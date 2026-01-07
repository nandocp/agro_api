from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.exc import IntegrityError

# from psycopg.errors import UniqueViolation
from agro_api.schemas.estate import (
    EstateCreate,
    EstateFilter,
    EstateItem,
    EstatesList,
    EstateUpdate,
)
from agro_api.services.estate import EstateService
from config.database import session
from config.user import current_user

router = APIRouter(prefix='/estate_plots', tags=['estate_plots'])
filters = Annotated[EstateFilter, Query()]


@router.post('/', response_model=EstateItem, status_code=HTTPStatus.CREATED)
async def create(session: session, user: current_user, estate: EstateCreate):
    try:
        service = await EstateService(session, user).create(estate)
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_CONTENT,
            detail='Slug already exists'
        )

    return service


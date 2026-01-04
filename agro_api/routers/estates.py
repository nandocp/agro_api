from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

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

router = APIRouter(prefix='/estates', tags=['estates'])
filters = Annotated[EstateFilter, Query()]


@router.post('/', response_model=EstateItem, status_code=HTTPStatus.CREATED)
async def create(session: session, user: current_user, estate: EstateCreate):
    service = await EstateService(session, user).create(estate)

    if isinstance(estate, dict):
        raise HTTPException(**service)

    return service


@router.get('/', response_model=EstatesList, status_code=HTTPStatus.OK)
async def index(session: session, user: current_user, filters: filters):
    return await EstateService(session, user).get_many(filters)


@router.get('/{estate_id}', response_model=EstateItem)
async def show(session: session, user: current_user, estate_id: str):
    estate = await EstateService(session, user).get_one(estate_id)

    if not estate:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Estate not found'
        )

    return estate


@router.put('/{estate_id}', response_model=EstateItem)
async def update(
    params: EstateUpdate, user: current_user, estate_id: str, session: session
):
    estate = await EstateService(session, user).update(estate_id, params)

    if not estate:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Estate not found'
        )

    return estate

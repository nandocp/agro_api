from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Request

from agro_api.schemas.common import BaseSchema
from agro_api.schemas.user import UserCreate, UserItem, UserUpdate
from agro_api.services.user import UserService
from config.database import session
from config.user import current_user, validate_current_user

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=BaseSchema)
async def create(user: UserCreate, session: session):
    service = await UserService(session).create(user)

    if not service:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='User already exists'
        )

    return service


@router.get('/{user_id}', status_code=HTTPStatus.OK, response_model=UserItem)
async def show(
    user_id: str, user: current_user, session: session, request: Request
):
    validate_current_user(user_id, str(user.id))
    return await UserService(session, user).get_one(user_id)


@router.put('/{user_id}', status_code=HTTPStatus.OK, response_model=UserItem)
async def update(
    user_id: str, user_data: UserUpdate, user: current_user, session: session
):
    validate_current_user(user_id, str(user.id))
    return await UserService(session, user).update(user_data)

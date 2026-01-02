from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from agro_api.schemas.user import (
    UserGetResponseSchema,
    UserPostPayloadSchema,
    UserPostResponseSchema,
    UserUpdatePayloadSchema,
    UserUpdateResponseSchema,
)
from agro_api.services.user import UserService
from config.database import session
from config.user import current_user, validate_current_user

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/',
    status_code=HTTPStatus.CREATED,
    response_model=UserPostResponseSchema
)
def create(user: UserPostPayloadSchema, session: session):
    service = UserService(session).create(user)

    if not service:
        raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='User already exists'
            )

    return service


@router.get('/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserGetResponseSchema
)
def show(user_id: str, current_user: current_user, session: session):
    validate_current_user(user_id, str(current_user.id))
    return current_user


@router.put('/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserUpdateResponseSchema
)
def update(
    user_id: str,
    user_data: UserUpdatePayloadSchema,
    current_user: current_user,
    session: session
):
    validate_current_user(user_id, str(current_user.id))
    return UserService(session).update(user_id, user_data)

# def index():

# def delete():

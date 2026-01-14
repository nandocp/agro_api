from http import HTTPStatus

from fastapi import APIRouter

from agro_api.endpoints import users as users_endpoint
from agro_api.schemas.user import UserItem

router = APIRouter(prefix='/users', tags=['users'])


router.add_api_route(
    '/',
    users_endpoint.create_user,
    methods=['POST'],
    response_model=UserItem,
    status_code=HTTPStatus.CREATED,
    summary='Register new User',
)

router.add_api_route(
    '/{user_id}',
    users_endpoint.get_user,
    methods=['GET'],
    response_model=UserItem,
    status_code=HTTPStatus.OK,
    summary='Get User',
    description='Get User by id',
)

router.add_api_route(
    '/{user_id}',
    users_endpoint.update_user,
    methods=['PUT', 'POST'],
    response_model=UserItem,
    status_code=HTTPStatus.OK,
    summary='Get User',
    description='Update User by id',
)

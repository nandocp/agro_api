from http import HTTPStatus
from uuid import UUID

# from uuid import UUID
from fastapi import APIRouter, Depends

from app.domain.accounts.schemas import UserFilters, UserResponse
from app.domain.accounts.services import UserService
from app.shared.dependencies import CurrentUser, SessionWithCommit
from app.shared.schemas import PaginatedResponse

router = APIRouter(tags=['users'])


@router.get(
    '',
    response_model=PaginatedResponse[UserResponse],
    status_code=HTTPStatus.OK,
)
async def list_users(
    session: SessionWithCommit,
    current_user: CurrentUser,
    filters: UserFilters = Depends(),
):
    return await UserService(session).index(filters, current_user=current_user)


@router.get(
    '/{user_id}',
    response_model=UserResponse,
    status_code=HTTPStatus.OK,
)
async def show_user(
    session: SessionWithCommit, current_user: CurrentUser, user_id: UUID
):
    return await UserService(session).show(user_id, current_user=current_user)

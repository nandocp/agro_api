from http import HTTPStatus

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


# @router.get(
#     '/{account_id}', response_model=Response, status_code=HTTPStatus.OK
# )
# async def show_account(
#     account_id, session: SessionWithCommit, current_user: CurrentUser
# ):
#     return await AccountService(session).show(
#         account_id, current_user=current_user
#     )


# @router.patch(
#     '/{account_id}/plan', response_model=Response, status_code=HTTPStatus.OK
# )
# async def update_plan(
#     data: AccountUpdatePlan,
#     session: SessionWithCommit,
#     account_id: UUID,
#     current_user: CurrentUser,
# ):
#     return await AccountService(session).update_plan(
#         data, account_id, current_user=current_user
#     )


# @router.patch('/{account_id}/archive', status_code=HTTPStatus.NO_CONTENT)
# async def archive_account(
#     session: SessionWithCommit, account_id: UUID, current_user: CurrentUser
# ):
#     return await AccountService(session).archive(
#         account_id, current_user=current_user
#     )


# @router.delete('/{account_id}', status_code=HTTPStatus.NO_CONTENT)
# async def delete_account(
#     session: SessionWithCommit, account_id: UUID, current_user: CurrentUser
# ):
#     return await AccountService(session).delete(
#         account_id, current_user=current_user
#     )

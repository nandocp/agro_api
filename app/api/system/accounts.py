from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends

from app.domain.accounts.schemas import (
    AccountCreate,
    AccountFilters,
    AccountUpdatePlan,
    UserCreateForm,
)
from app.domain.accounts.schemas import AccountResponse as Response
from app.domain.accounts.services import AccountService, UserService
from app.shared.dependencies import CurrentUser, SessionWithCommit
from app.shared.schemas import BaseSchema, PaginatedResponse

router = APIRouter(tags=['accounts'])


@router.get(
    '', response_model=PaginatedResponse[Response], status_code=HTTPStatus.OK
)
async def list_accounts(
    session: SessionWithCommit,
    current_user: CurrentUser,
    filters: AccountFilters = Depends(),
):
    return await AccountService(session).index(
        filters, current_user=current_user
    )


@router.get(
    '/{account_id}', response_model=Response, status_code=HTTPStatus.OK
)
async def show_account(
    account_id, session: SessionWithCommit, current_user: CurrentUser
):
    return await AccountService(session).show(
        account_id, current_user=current_user
    )


@router.post('', response_model=Response, status_code=HTTPStatus.CREATED)
async def create_account(
    data: AccountCreate, session: SessionWithCommit, current_user: CurrentUser
):
    return await AccountService(session).create(
        data, current_user=current_user
    )


@router.patch(
    '/{account_id}/plan', response_model=Response, status_code=HTTPStatus.OK
)
async def update_plan(
    data: AccountUpdatePlan,
    session: SessionWithCommit,
    account_id: UUID,
    current_user: CurrentUser,
):
    return await AccountService(session).update_plan(
        data, account_id, current_user=current_user
    )


@router.patch('/{account_id}/archive', status_code=HTTPStatus.NO_CONTENT)
async def archive_account(
    session: SessionWithCommit, account_id: UUID, current_user: CurrentUser
):
    return await AccountService(session).archive(
        account_id, current_user=current_user
    )


@router.delete('/{account_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_account(
    session: SessionWithCommit, account_id: UUID, current_user: CurrentUser
):
    return await AccountService(session).delete(
        account_id, current_user=current_user
    )


@router.post(
    '/{account_id}/users',
    status_code=HTTPStatus.CREATED,
    response_model=BaseSchema,
)
async def create_account_user(
    account_id: UUID,
    current_user: CurrentUser,
    data: UserCreateForm,
    session: SessionWithCommit,
):
    return await UserService(session).create(
        data, account_id, current_user=current_user
    )

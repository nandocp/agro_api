from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends

from app.domain.accounts.schemas import (
    AccountCreate,
    AccountFilters,
    AccountUpdatePlan,
)
from app.domain.accounts.schemas import AccountResponse as Response
from app.domain.accounts.services import AccountService
from app.shared.dependencies import SessionWithCommit
from app.shared.schemas import PaginatedResponse

router = APIRouter(tags=['accounts'])


@router.get(
    '', response_model=PaginatedResponse[Response], status_code=HTTPStatus.OK
)
async def list_accounts(
    session: SessionWithCommit, filters: AccountFilters = Depends()
):
    return await AccountService(session).index(filters)


@router.get(
    '/{account_id}', response_model=Response, status_code=HTTPStatus.OK
)
async def show_account(account_id, session: SessionWithCommit):
    return await AccountService(session).show(account_id)


@router.post('', response_model=Response, status_code=HTTPStatus.CREATED)
async def create_account(data: AccountCreate, session: SessionWithCommit):
    return await AccountService(session).create(data)


@router.patch(
    '/{account_id}/plan', response_model=Response, status_code=HTTPStatus.OK
)
async def update_plan(
    data: AccountUpdatePlan, session: SessionWithCommit, account_id: UUID
):
    return await AccountService(session).update_plan(data, account_id)

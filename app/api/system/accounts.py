from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter

from app.domain.accounts.schemas import AccountCreate, AccountUpdatePlan
from app.domain.accounts.schemas import AccountResponse as Response
from app.domain.accounts.services import AccountService
from app.shared.dependencies import SessionWithCommit

router = APIRouter(tags=['accounts'])


@router.post('', response_model=Response, status_code=HTTPStatus.CREATED)
async def create(data: AccountCreate, session: SessionWithCommit):
    return await AccountService(session).create(data)


@router.patch(
    '/{account_id}/plan', response_model=Response, status_code=HTTPStatus.OK
)
async def update_plan(
    data: AccountUpdatePlan, session: SessionWithCommit, account_id: UUID
):
    return await AccountService(session).update_plan(data, account_id)


@router.get(
    '/{account_id}', response_model=Response, status_code=HTTPStatus.OK
)
async def show(account_id, session: SessionWithCommit):
    return await AccountService(session).show(account_id)

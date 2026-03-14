from http import HTTPStatus

from fastapi import APIRouter

from app.domain.accounts.models import Account
from app.domain.accounts.schemas import AccountCreate, AccountResponse
from app.domain.accounts.services import AccountService
from app.shared.dependencies import SessionWithCommit

router = APIRouter(tags=['accounts'])


@router.post(
    '', response_model=AccountResponse, status_code=HTTPStatus.CREATED
)
async def create_account(data: AccountCreate, session: SessionWithCommit):
    return await AccountService(Account, session).create_account(data)

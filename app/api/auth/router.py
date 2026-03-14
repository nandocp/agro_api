from http import HTTPStatus

from fastapi import APIRouter

from app.domain.accounts.schemas import LoginRequest, TokenResponse
from app.domain.accounts.services import UserService
from app.shared.dependencies import SessionWithCommit

router = APIRouter(tags=['auth'])


@router.post('/login', response_model=TokenResponse)
async def login(session: SessionWithCommit, form_data: LoginRequest):
    service = await UserService(session).login(form_data)
    return TokenResponse(access_token=service.token)


@router.delete('/logout', status_code=HTTPStatus.NO_CONTENT)
async def logout(session: SessionWithCommit):
    pass
    # await UserService(Session).logout(user)

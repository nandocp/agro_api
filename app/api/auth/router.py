from http import HTTPStatus

from fastapi import APIRouter, Depends

from app.domain.accounts.schemas import LoginRequest, TokenResponse
from app.domain.accounts.services import UserService
from app.shared.dependencies import (
    CurrentUser,
    OAuth2Scheme,
    SessionWithCommit,
)

router = APIRouter(tags=['auth'])


@router.post('/login', response_model=TokenResponse)
async def login(session: SessionWithCommit, form_data: LoginRequest):
    token = await UserService(session).login(form_data)
    return TokenResponse(access_token=token)


@router.post('/refresh_token', response_model=TokenResponse)
async def refresh_token(
    session: SessionWithCommit,
    token: str = Depends(OAuth2Scheme),
):
    token = await UserService(session).refresh_token(token)
    return TokenResponse(access_token=token)


@router.delete('/logout', status_code=HTTPStatus.NO_CONTENT)
async def logout(session: SessionWithCommit, current_user: CurrentUser):
    await UserService(session).logout(current_user)

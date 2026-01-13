from http import HTTPStatus

from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from agro_api.services.auth import AuthService
from config.authentication import current_user
from config.database import session

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/login', status_code=HTTPStatus.NO_CONTENT)
async def login(
    response: Response,
    session: session,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    service = await AuthService(session).login(form_data)

    response.headers['Authorization'] = service
    response.headers['Authorization-Type'] = 'Bearer'


@router.delete('/logout', status_code=HTTPStatus.NO_CONTENT)
async def logout(session: session, user: current_user):
    await AuthService(session).logout(user)

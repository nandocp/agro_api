from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm

from agro_api.services.auth import AuthService
from config.database import session
from config.user import current_user

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/login', status_code=HTTPStatus.NO_CONTENT)
def login(
    response: Response,
    session: session,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    service = AuthService(session).login(form_data)

    if isinstance(service, dict):
        raise HTTPException(**service)

    response.headers['Authorization'] = service
    response.headers['Authorization-Type'] = 'Bearer'


@router.post('/logout', status_code=HTTPStatus.NO_CONTENT)
def logout(session: session, current_user: current_user):
    pass

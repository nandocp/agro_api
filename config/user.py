from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError
from sqlalchemy.orm import Session

from agro_api.entities.user import User
from agro_api.services.user import UserService
from config.database import get_session
from config.jwt import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


def get_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    try:
        payload = decode_access_token(token)
        jti = payload.get('jti')
        sub = payload.get('sub')

        if not sub or not jti:
            raise credentials_exception
    except DecodeError:
        raise credentials_exception

    user = UserService(session).get_one(jti=jti, id=sub)
    if not user:
        raise credentials_exception

    return user


def validate_current_user(target_id, user_id):
    if target_id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='You shall not do it'
        )

    return True


current_user = Annotated[User, Depends(get_user)]

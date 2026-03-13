from http import HTTPStatus

from app.repositories.core import AuthRepository
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError
from sqlalchemy.orm import Session

from app.domain.accounts.models import User
from config.database import get_session
from config.jwt import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


async def get_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
) -> User:
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode_access_token(token)
        jti = payload.get('jti')
        sub = payload.get('sub')

        if not sub or not jti:
            raise credentials_exception
    except DecodeError:
        raise credentials_exception

    user = await AuthRepository(User, session).find_by_jti(jti)
    if not user or str(user.id) != sub:
        raise credentials_exception

    return user


def validate_current_user(target_id, user_id):
    if target_id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail='You shall not do it'
        )

    return True

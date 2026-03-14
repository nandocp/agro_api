from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.accounts.auth import decode_access_token
from app.domain.accounts.models import User
from app.shared.crud import CRUDBase
from config.database import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


async def get_current_user(
    session: AsyncSession = Depends(get_session),
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

    user = await CRUDBase[User](User, session).get_by({'jti': jti})
    if not user or str(user.id) != sub:
        raise credentials_exception

    return user

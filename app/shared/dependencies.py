from http import HTTPStatus
from typing import Annotated, Type, TypeVar

from fastapi import Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.accounts.auth import decode_access_token
from app.domain.accounts.models import User
from app.shared.crud import CRUDBase
from config.database import engine
from config.logging import logger

FilterSchemaType = TypeVar('FilterSchemaType', bound=BaseModel)


def log_error(error: Exception):
    logger.error(f'DB operation failed with {error}. Auto-rollbacking...')


async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        try:
            yield session
        except Exception as error:
            log_error(error)
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_session_with_commit():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        try:
            yield session
            await session.commit()
        except Exception as error:
            log_error(error)
            await session.rollback()
            raise
        finally:
            await session.close()


OAuth2Scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


async def get_current_user(
    session: AsyncSession = Depends(get_session),
    token: str = Depends(OAuth2Scheme),
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


def filters(filter_schema: Type[FilterSchemaType]):
    return Annotated[filter_schema, Query()]


Session = Annotated[AsyncSession, Depends(get_session)]
SessionWithCommit = Annotated[AsyncSession, Depends(get_session_with_commit)]
CurrentUser = Annotated[User, Depends(get_current_user)]

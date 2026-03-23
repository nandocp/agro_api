from typing import Annotated, TypeVar

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.accounts.auth import (
    decode_and_validate_token,
)
from app.domain.accounts.models import Role, User
from app.shared.exceptions import InvalidCredentialsError
from config.database import engine
from config.logging import logger

FilterSchemaType = TypeVar('FilterSchemaType', bound=BaseModel)


def log_error(error: Exception):  # pragma: no cover
    logger.error(f'DB operation failed with {error}. Auto-rollbacking...')


async def get_session():  # pragma: no cover
    async with AsyncSession(engine, expire_on_commit=False) as session:
        try:
            yield session
        except Exception as error:
            log_error(error)
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_session_with_commit():  # pragma: no cover
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
    sub, jti = decode_and_validate_token(token)

    user = await session.scalar(
        select(User)
        .where(User.jti == jti)
        .options(
            selectinload(User.roles).selectinload(Role.permissions),
            selectinload(User.account),
        )
    )

    if not user or str(user.id) != sub:
        raise InvalidCredentialsError

    return user


Session = Annotated[AsyncSession, Depends(get_session)]
SessionWithCommit = Annotated[AsyncSession, Depends(get_session_with_commit)]
CurrentUser = Annotated[User, Depends(get_current_user)]

from typing import Annotated
from warnings import warn

from fastapi import Depends

# from sqlalchemy import Engine, create_engine
# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from config.settings import settings

engine: AsyncEngine = create_async_engine(
    str(settings.DATABASE_URL),
    plugins=["geoalchemy2"],
    pool_pre_ping=True,
    max_overflow=64,
    echo=settings.DEBUG,
)


async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        try:
            yield session
        except Exception as error:
            print(error)
            warn('DB operation failed. Auto-rollbacking...')
            await session.rollback()
        finally:
            await session.close()


session = Annotated[AsyncSession, Depends(get_session)]

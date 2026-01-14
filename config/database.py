from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import registry

from config.logging import logger
from config.settings import settings

engine: AsyncEngine = create_async_engine(
    str(settings.DATABASE_URL),
    plugins=['geoalchemy2'],
    pool_pre_ping=True,
    max_overflow=64,
    echo=settings.DEBUG,
)


async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        try:
            yield session
        except Exception as error:
            logger.warn(
                f'DB operation failed with {error}. Auto-rollbacking...'
            )
            await session.rollback()
        finally:
            await session.close()


session = Annotated[AsyncSession, Depends(get_session)]
table_registry = registry()

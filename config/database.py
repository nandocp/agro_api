from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from config.logging import logger
from config.settings import settings

engine: AsyncEngine = create_async_engine(
    str(settings.DATABASE_URL),
    plugins=['geoalchemy2'],
    pool_pre_ping=True,
    max_overflow=64,
    echo=settings.DEBUG,
)


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

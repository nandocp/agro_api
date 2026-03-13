import asyncio
from urllib.parse import urlparse

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from config.settings import settings


async def create_database() -> None:
    default_url = str(settings.DATABASE_URL).rsplit('/', 1)[0] + '/postgres'
    engine = create_async_engine(default_url, isolation_level='AUTOCOMMIT')
    db_name = urlparse(str(settings.DATABASE_URL)).path.lstrip('/')

    async with engine.connect() as conn:
        exists = await conn.execute(
            text('SELECT 1 FROM pg_database WHERE datname = :name'),
            {'name': db_name},
        )
        if not exists.scalar():
            await conn.execute(text(f'CREATE DATABASE "{db_name}"'))
            print(f'Database {db_name} created.')
        else:
            print(f'Database {db_name} already exists.')

    await engine.dispose()


if __name__ == '__main__':
    asyncio.run(create_database())

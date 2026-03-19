import asyncio
from sys import argv
from urllib.parse import urlparse

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from config.settings import settings


async def drop_database() -> None:
    default_url = str(settings.DATABASE_URL).rsplit('/', 1)[0] + '/postgres'
    engine = create_async_engine(default_url, isolation_level='AUTOCOMMIT')
    db_name = urlparse(str(settings.DATABASE_URL)).path.lstrip('/')

    ENV_SET = 2
    if len(argv) == ENV_SET:
        db_name = f'{db_name}_{argv[1]}'

    async with engine.connect() as conn:
        await conn.execute(
            text("""
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE datname = :name AND pid <> pg_backend_pid()
            """),
            {'name': db_name},
        )
        await conn.execute(text(f'DROP DATABASE IF EXISTS "{db_name}"'))
        print(f'Database {db_name} dropped.')

    await engine.dispose()


if __name__ == '__main__':
    asyncio.run(drop_database())

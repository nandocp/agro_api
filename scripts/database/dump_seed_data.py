# scripts/dump_seed_data.py
import asyncio
import subprocess

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

import app.shared.registry  # noqa: F401
from app.shared.model.base import DeclarativeModel
from config.settings import settings
from seeds.production.organism_traits import seed as seed_traits
from seeds.production.rbac import seed as seed_rbac
from seeds.production.soil_classifications import seed as seed_soil

SEED_TABLES = [
    'roles',
    'permissions',
    'role_permissions',
    'organism_traits',
    'soil_classifications',
]

DB_NAME = 'agro_db_seed'
SEED_DATABASE_URL = settings.DATABASE_URL.rsplit('/', 1)[0] + f'/{DB_NAME}'


async def create_seed_database() -> None:
    default_url = SEED_DATABASE_URL.rsplit('/', 1)[0] + '/postgres'
    engine = create_async_engine(default_url, isolation_level='AUTOCOMMIT')
    async with engine.connect() as conn:
        await conn.execute(text(f'CREATE DATABASE {DB_NAME};'))
    await engine.dispose()
    print('✓ Seed database created')


async def apply_schema_and_seeds() -> None:
    engine = create_async_engine(
        SEED_DATABASE_URL,
        plugins=['geoalchemy2'],
    )

    async with engine.begin() as conn:
        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS postgis'))
        await conn.run_sync(DeclarativeModel.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        await seed_rbac(session)
        await seed_soil(session)
        await seed_traits(session)
        await session.commit()

    await engine.dispose()
    print('✓ Schema and seeds applied')


def dump_seed_data(output: str = 'migrations/seed_data.sql') -> None:
    pg_url = SEED_DATABASE_URL.replace(
        'postgresql+psycopg://', 'postgresql://'
    )
    table_args = []
    for table in SEED_TABLES:
        table_args.extend(['-t', table])

    result = subprocess.run(
        [
            'pg_dump',
            '--data-only',
            '--disable-triggers',
            '--no-owner',
            '--no-privileges',
            *table_args,
            pg_url,
            '-f',
            output,
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        print(f'✓ Seed data dumped to {output}')
    else:
        raise RuntimeError(f'Seed data dump failed: {result.stderr}')


async def drop_seed_database() -> None:
    default_url = SEED_DATABASE_URL.rsplit('/', 1)[0] + '/postgres'
    engine = create_async_engine(default_url, isolation_level='AUTOCOMMIT')
    async with engine.connect() as conn:
        # encerra conexões ativas
        await conn.execute(
            text(f"""
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = '{DB_NAME}'
            AND pid <> pg_backend_pid()
        """)
        )
        await conn.execute(text(f'DROP DATABASE IF EXISTS {DB_NAME}'))
    await engine.dispose()
    print('✓ Seed database dropped')


async def main() -> None:
    try:
        await create_seed_database()
        await apply_schema_and_seeds()
        dump_seed_data()
    finally:
        await drop_seed_database()  # sempre dropa, mesmo em caso de erro


if __name__ == '__main__':
    asyncio.run(main())

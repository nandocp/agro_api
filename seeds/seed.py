import asyncio
import importlib
import pkgutil
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

import app.shared.registry  # noqa: F401
from config.settings import settings

"""
Discovers and runs all seed modules for the current environment.
Each module must implement an async `seed(session)` function.
"""


async def run_seeds(session: AsyncSession) -> None:
    environment = settings.ENVIRONMENT
    seeds_dir = Path(__file__).parent

    # always run production seeds
    await _run_directory(session, seeds_dir / 'production')

    # run development seeds only in development or test environment
    dev_envs = ['development', 'test']
    if environment in dev_envs:
        await _run_directory(session, seeds_dir / 'development')


async def _run_directory(session: AsyncSession, directory: Path) -> None:
    print(f'📁 Seeding files from directory {directory}')

    if not directory.exists():
        print(f'⚠️ Directory {directory} not found. Skipping')
        return

    package_name = f'seeds.{directory.name}'

    for _, module_name, _ in pkgutil.iter_modules([str(directory)]):
        full_module_name = f'{package_name}.{module_name}'
        module = importlib.import_module(full_module_name)

        if not hasattr(module, 'seed'):
            print(f'⚠️ {full_module_name} has no seed() function. Skipping')
            continue

        print(f'🌱 Seeding {full_module_name}')
        await module.seed(session)
        print(f'🗄️ {full_module_name} seeding completed')


async def main() -> None:
    engine = create_async_engine(settings.DATABASE_URL)
    async with AsyncSession(engine, expire_on_commit=False) as session:
        await run_seeds(session)
        await session.commit()
        print('\n✅ All seeds completed successfully')
    await engine.dispose()


if __name__ == '__main__':
    asyncio.run(main())

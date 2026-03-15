from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from config.settings import settings

engine: AsyncEngine = create_async_engine(
    str(settings.DATABASE_URL),
    plugins=['geoalchemy2'],
    pool_pre_ping=True,
    max_overflow=64,
    echo=settings.DEBUG,
    connect_args={'options': '-c timezone=UTC'},
)

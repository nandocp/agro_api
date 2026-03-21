import os
from secrets import token_hex
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import selectinload
from testcontainers.postgres import PostgresContainer

from app.domain.accounts.auth import create_access_token
from app.domain.accounts.models import Role, User, user_roles
from app.main import app
from app.shared.dependencies import get_session, get_session_with_commit
from seeds.production.organism_traits import seed as seed_traits
from seeds.production.rbac import seed as seed_rbac
from seeds.production.soil_classifications import seed as seed_soil
from tests.factories.accounts import AccountFactory, UserFactory
from tests.factories.estates import EstateFactory
from tests.factories.fields import FieldFactory

os.environ.setdefault(
    'DOCKER_HOST', f'unix:///run/user/{os.getuid()}/podman/podman.sock'
)
os.environ.setdefault('TESTCONTAINERS_RYUK_DISABLED', 'true')


@pytest.fixture(scope='session')
def postgres_container():
    with PostgresContainer(
        image='localhost/agro_api-test-db:latest',
        username='test',
        password='test',
        dbname='agro_api_test',
    ) as container:
        yield container


# Engine compartilhada em toda a sessão
@pytest_asyncio.fixture(scope='session')
async def engine(postgres_container):
    db_url = postgres_container.get_connection_url().replace(
        'postgresql+psycopg2://', 'postgresql+psycopg://'
    )
    engine: AsyncEngine = create_async_engine(
        db_url,
        plugins=['geoalchemy2'],
    )

    # async with engine.begin() as conn:
    #     await conn.run_sync(DeclarativeModel.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        await seed_rbac(session)
        await seed_soil(session)
        await seed_traits(session)
        await session.commit()

    yield engine

    # sem drop_all — container é destruído pelo testcontainers no teardown
    await engine.dispose()


@pytest_asyncio.fixture(scope='function')
async def session(engine):
    async with engine.connect() as conn:
        await conn.begin_nested()  # savepoint
        async with AsyncSession(bind=conn, expire_on_commit=False) as session:
            yield session
            await conn.rollback()  # rollback after each test


@pytest_asyncio.fixture
async def client(session):
    async def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_session_with_commit] = get_session_override
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://localhost:8000'
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def token(user, session) -> str:
    user.jti = uuid4()
    session.add(user)
    await session.commit()
    return create_access_token(sub=user.id, jti=user.jti)


@pytest_asyncio.fixture
async def user(session, account):
    user = await UserFactory.create(
        session, account_id=account.id, pwd=token_hex(4)
    )

    user_with_role = await session.scalar(
        select(User)
        .where(User.id == user.id)
        .options(
            selectinload(User.roles).selectinload(Role.permissions),
            selectinload(User.account),
        )
    )
    return user_with_role


@pytest_asyncio.fixture
async def admin_user(session, account) -> User:
    user = await UserFactory.create(session, account_id=account.id)
    role = await session.scalar(select(Role).where(Role.name == 'admin'))

    await session.execute(
        insert(user_roles).values(user_id=user.id, role_id=role.id)
    )
    await session.flush()

    user_with_role = await session.scalar(
        select(User)
        .where(User.id == user.id)
        .options(
            selectinload(User.roles).selectinload(Role.permissions),
            selectinload(User.account),
        )
    )
    return user_with_role


@pytest_asyncio.fixture
async def account(session) -> AccountFactory:
    return await AccountFactory.create(session)


@pytest_asyncio.fixture
async def estate(session, account) -> EstateFactory:
    return await EstateFactory.create(session, account_id=account.id)


@pytest_asyncio.fixture
async def field(session, estate, user) -> EstateFactory:
    return await FieldFactory.create(
        session, estate_id=estate.id, creator_id=user.id
    )

from secrets import token_hex
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

# from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool

from app.domain.accounts.auth import create_access_token
from app.main import app
from app.shared.dependencies import get_session, get_session_with_commit
from app.shared.model.declarative import DeclarativeModel
from config.settings import settings
from tests.factories.accounts import AccountFactory, UserFactory
from tests.factories.estates import EstateFactory


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
async def session():
    engine: AsyncEngine = create_async_engine(
        f'{settings.DATABASE_URL}_test',
        poolclass=StaticPool,
        plugins=['geoalchemy2'],
    )

    async with engine.begin() as conn:
        await conn.run_sync(DeclarativeModel.metadata.create_all)

    async with engine.connect() as conn:
        await conn.begin_nested()  # savepoint
        async with AsyncSession(bind=conn, expire_on_commit=False) as session:
            yield session
            await conn.rollback()  # rollback após cada teste

    async with engine.begin() as conn:
        await conn.run_sync(DeclarativeModel.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def persist(session):
    async def _persist():
        await session.commit()
        session.expire_all()

    return _persist


@pytest_asyncio.fixture
async def estate(session, account) -> EstateFactory:
    return await EstateFactory.create(session, account_id=account.id)


@pytest_asyncio.fixture
async def account(session) -> AccountFactory:
    return await AccountFactory.create(session)


@pytest_asyncio.fixture
async def token(user, session) -> str:
    user.jti = uuid4()
    session.add(user)
    await session.commit()
    return create_access_token({'sub': user.id, 'jti': user.jti}).jwt


@pytest.fixture
def password():
    return token_hex(4)


@pytest_asyncio.fixture
async def user(session, account, password):
    user = await UserFactory.create(
        session, account_id=account.id, pwd=password
    )

    return user


@pytest_asyncio.fixture
async def account(session) -> AccountFactory:
    return await AccountFactory.create(session)


@pytest_asyncio.fixture
async def main_account(session):
    return await AccountFactory()


# @pytest_asyncio.fixture
# async def main_user(session, main_account):
#     user = await UserFactory.build(account_id=main_account.id)


# @pytest_asyncio.fixture
# async def user(session):
#     password = token_hex(4)
#     user = UserFactory.build(pwd=password)
#     user.password = hash_password(password)
#     session.add(user)
#     await session.commit()
#     await session.refresh(user)

#     user.clean_password = password

#     return user


# @pytest_asyncio.fixture
# async def other_user(session):
#     password = token_hex(4)
#     user = UserFactory.build(pwd=password)
#     user.password = hash_password(password)
#     session.add(user)
#     await session.commit()
#     await session.refresh(user)

#     user.clean_password = password

#     return user

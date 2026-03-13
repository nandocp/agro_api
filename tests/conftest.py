# from secrets import token_hex

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

# from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool

from app.main import app
from app.shared.model.declarative import DeclarativeModel
from config.database import get_session
from config.settings import settings
from tests.factories.accounts import AccountFactory
from tests.factories.estates import EstateFactory


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override

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

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(DeclarativeModel.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def estate(session) -> EstateFactory:
    account = await AccountFactory.create(session)
    estate = await EstateFactory.create(session, account_id=account.id)
    return estate


# @pytest_asyncio.fixture
# async def token(client, user) -> str:
#     response = client.post(
#         '/auth/login',
#         data={'username': user.email, 'password': user.clean_password},
#     )

#     return response.headers['Authorization']


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

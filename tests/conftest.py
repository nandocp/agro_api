from contextlib import contextmanager
from datetime import datetime
from secrets import token_hex
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from agro_api.app import app
from agro_api.entities.base import table_registry
from config.database import get_session
from config.password import hash_password
from config.settings import settings
from tests.factories.users import UserFactory


@contextmanager
def _mock_db_time(model, columns=[], time=datetime.now()):
    def fake_time_hook(mapper, connection, target):
        for column in columns:
            if hasattr(target, column):
                setattr(target, column, time)

    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)


@contextmanager
def _mock_id(model, id=uuid4()):
    def fake_id_hook(mapper, connection, target):
        target.id = id

    event.listen(model, 'before_insert', fake_id_hook)

    yield id

    event.remove(model, 'before_insert', fake_id_hook)


@pytest.fixture
def mock_id():
    return _mock_id


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override

        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        f'{settings.DATABASE_URL}_test', poolclass=StaticPool
    )

    table_registry.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    password = token_hex(4)
    user = UserFactory.build(pwd=password)
    user.password = hash_password(password)
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
def other_user(session):
    password = token_hex(4)
    user = UserFactory.build(pwd=password)
    user.password = hash_password(password)
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
def token(client, user) -> str:
    response = client.post(
        '/auth/login',
        data={
            'username': user.email,
            'password': user.clean_password
        }
    )

    return response.headers['Authorization']

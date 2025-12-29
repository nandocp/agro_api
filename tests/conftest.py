from contextlib import contextmanager
from datetime import datetime
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from agro_api.app import app
from agro_api.entities.base import table_registry
from config.settings import settings


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
def client():
    return TestClient(app)


@pytest.fixture
def db_session():
    db_url = f'{settings.DATABASE_URL}_test'
    print(db_url)

    engine = create_engine(db_url)
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)

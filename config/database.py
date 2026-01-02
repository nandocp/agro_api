from typing import Annotated
from warnings import warn

from fastapi import Depends
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from config.settings import settings

engine: Engine = create_engine(
    str(settings.DATABASE_URL), pool_pre_ping=True, max_overflow=64
)


def get_session():
    with Session(engine) as session:
        try:
            yield session
        except Exception as error:
            print(error)
            warn('DB operation failed. Auto-rollbacking...')
            session.rollback()
        finally:
            session.close()


session = Annotated[Session, Depends(get_session)]

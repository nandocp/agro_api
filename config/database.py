# from contextlib import contextmanager
# from warnings import warn

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from config.settings import settings

engine: Engine = create_engine(
    str(settings.DATABASE_URL), pool_pre_ping=True, max_overflow=64
)

# local_session: Session = sessionmaker(
#     autocommit=False, autoflush=False, bind=engine
# )


# @contextmanager
# def db_session():
#     db = local_session()

#     try:
#         yield db
#     except Exception as e:
#         print(e)
#         warn('DB operation failed. Auto-rollbacking...')
#         db.rollback()
#     finally:
#         db.close()


def get_session():
    print('antes do with Session')
    with Session(engine) as session:
        print('dentro do with Session')
        print(session)
        yield session


# class DBConnection:
#     def __init__(self) -> None:
#         self.__engine = self.__create_engine()
#         self.session = None

#     @classmethod
#     def __create_engine(self) -> Engine:
#         return create_engine(str(settings.DATABASE_URL), pool_pre_ping=True)

#     def get_engine(self) -> Engine:
#         return self.__engine

#     def __enter__(self):
#         self.session = sessionmaker(
#             autocommit=False, autoflush=False, bind=self.__engine
#         )

#         return self

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         print(exc_type, exc_tb, exc_val)
#         self.session.object_session().close()
#         # self.session.close()

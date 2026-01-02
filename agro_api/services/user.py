from sqlalchemy import select

from agro_api.entities.user import User
from config.password import hash_password

from .base import BaseService


class UserService(BaseService):
    def __init__(self, session=None):
        super().__init__(User, session)

    def create(self, schema_params):
        schema_params.password = hash_password(schema_params.password)
        db_user = self.find_by_email(schema_params.email)

        if db_user:
            return False

        new_user = User(**schema_params.model_dump())

        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)

        return new_user

    def get_one(self, id: str, jti: str):
        user = self.find_by_jti(jti)

        if not user or str(user.id) != id:
            return False

        return user

    def get_many(self, *, skip: int = 0, limit: int = 100):
        pass

    def update(self, user_id, params):
        db_user = self.session.scalar(select(User).where(User.id == user_id))

        if not db_user:
            return False

        db_user.name = params.name
        self.session.commit()
        self.session.refresh(db_user)

        return db_user

    def remove(self, *, id: int):
        pass

    def find_by_email(self, email) -> User:
        return self.session.scalar(select(User).where(User.email == email))

    def find_by_jti(self, jti) -> User | None:
        return self.session.scalar(select(User).where(User.jti == jti))

from sqlalchemy import select

from agro_api.entities.user import User
from config.password import hash_password

from .base import BaseService


class UserService(BaseService):
    def __init__(self, session=None):
        super().__init__(User, session)

    async def create(self, schema_params):
        schema_params.password = hash_password(schema_params.password)
        db_user = await self.find_by_email(schema_params.email)

        if db_user:
            return False

        new_user = User(**schema_params.model_dump())

        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)

        return new_user

    async def get_one(self, id: str, jti: str):
        user = await self.find_by_jti(jti)

        if not user or str(user.id) != id:
            return False

        return user

    async def get_many(self, *, skip: int = 0, limit: int = 100):
        pass  # pragma: no cover

    async def update(self, user_id, params):
        db_user = await self.session.scalar(
            select(User).where(User.id == user_id)
        )

        if not db_user:
            return False

        db_user.name = params.name
        await self.session.commit()
        await self.session.refresh(db_user)

        return db_user

    async def remove(self, *, id: int):
        pass  # pragma: no cover

    async def find_by_email(self, email) -> User:
        return await self.session.scalar(
            select(User).where(User.email == email)
        )

    async def find_by_jti(self, jti) -> User | None:
        return await self.session.scalar(
            select(User).where(User.jti == jti)
        )

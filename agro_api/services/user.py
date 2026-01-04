from sqlalchemy import select

from agro_api.entities.user import User
from agro_api.services.base import BaseService
from config.password import hash_password


class UserService(BaseService):
    def __init__(self, session=None, user=None):
        super().__init__(User, session, user)

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

    async def get_one(self, user_id: str):
        # eventualmente implementar caso de admin user

        return self.user

    async def get_many(self, *, skip: int = 0, limit: int = 100):
        # eventualmente implementar caso de admin user
        pass  # pragma: no cover

    async def update(self, params):
        self.user.name = params.name
        self.session.add(self.user)
        await self.session.commit()
        await self.session.refresh(self.user)

        return self.user

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

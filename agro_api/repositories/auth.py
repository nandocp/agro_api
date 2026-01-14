from uuid import UUID

from sqlalchemy import select

from agro_api.entities.core import User
from agro_api.repositories.base import BaseRepository
from agro_api.schemas.auth import AuthLogin


class AuthRepository(BaseRepository):
    async def login(self, user: AuthLogin) -> True:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return True

    async def logout(self, user: User) -> True:
        self.session.add(user)
        await self.session.commit()

        return True

    async def find_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        return await self.session.scalar(query)

    async def find_by_jti(self, jti: UUID) -> User | None:
        query = select(User).where(User.jti == jti)
        return await self.session.scalar(query)

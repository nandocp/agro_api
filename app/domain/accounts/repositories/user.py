from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.domain.accounts.models import User
from app.domain.accounts.schemas import UserCreate, UserUpdate
from app.shared.crud import CRUDBase


class UserRepository(CRUDBase[User, UserCreate, UserUpdate]):
    def __init__(self, session):
        super().__init__(User, session)

    async def get_by_email_and_account(
        self, email: str, account_id: UUID
    ) -> User | None:
        result = await self.session.execute(
            select(User).where(
                User.email == email,
                User.account_id == account_id,
                User.deactivated_at.is_(None),
            )
        )
        return result.scalar_one_or_none()

    async def get_with_relations(self, user_id: UUID) -> User | None:
        return await self.session.scalar(
            select(User)
            .where(User.id == user_id)
            .options(
                selectinload(User.roles),
                selectinload(User.account),
                selectinload(User.created_activities),
            )
        )

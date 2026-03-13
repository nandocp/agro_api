from uuid import UUID

from sqlalchemy import select

from app.domain.accounts.models import User
from app.shared.crud_base import CRUDBase


class UserRepository(CRUDBase[User]):
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

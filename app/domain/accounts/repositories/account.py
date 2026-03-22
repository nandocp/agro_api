from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.domain.accounts.models.account import Account
from app.domain.accounts.schemas.account import AccountCreate
from app.shared.crud import CRUDBase


class AccountRepository(CRUDBase[Account, AccountCreate]):
    def __init__(self, session):
        super().__init__(Account, session)

    async def get_with_relations(self, account_id: UUID) -> Account | None:
        return await self.session.scalar(
            select(Account)
            .where(Account.id == account_id)
            .options(
                # selectinload(Account.address),
                selectinload(Account.estates),
            )
        )

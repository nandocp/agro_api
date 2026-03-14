from app.domain.accounts.models import Account
from app.domain.accounts.schemas import AccountCreate, AccountUpdate
from app.shared.service import BaseService


class AccountService(BaseService[Account, AccountCreate, AccountUpdate]):
    async def create_account(self, object: AccountCreate):
        breakpoint()
        return await self.repo.create(object)

from uuid import UUID

from app.domain.accounts.models import Account
from app.domain.accounts.repositories import AccountRepository
from app.domain.accounts.schemas import (
    AccountCreate,
    AccountFilters,
    AccountUpdatePlan,
)
from app.shared.exceptions import NotFoundError
from app.shared.schemas import PaginatedResponse
from app.shared.service import BaseService
from app.shared.utils import sanitize_filters


class AccountService(BaseService):
    def __init__(self, session):
        super().__init__(session)
        self.repo = AccountRepository(session)

    async def create(self, account_create: AccountCreate):
        return await self.repo.create(account_create)

    async def update_plan(
        self,
        plan_update: AccountUpdatePlan,
        account_id: UUID,
    ):
        account = await self.repo.get_one(account_id)
        if not account:
            raise NotFoundError('account')

        return await self.repo.update(
            account, {'plan': plan_update.plan.value}
        )

    async def show(self, account_id: UUID) -> Account:
        account = await self.repo.get_with_relations(account_id)
        if not account:
            raise NotFoundError('account')

        return account

    async def index(
        self, filters: AccountFilters
    ) -> PaginatedResponse[Account]:
        clean_filters = sanitize_filters(filters)
        return await self.repo.get_many(
            filters=clean_filters, offset=filters.offset, limit=filters.limit
        )

from datetime import datetime, timezone
from uuid import UUID

from app.domain.accounts.models import Account, User
from app.domain.accounts.repositories import AccountRepository
from app.domain.accounts.schemas import (
    AccountCreate,
    AccountFilters,
    AccountUpdatePlan,
)
from app.shared.authorization import require_permission
from app.shared.enums import Action, Resource
from app.shared.exceptions import NotFoundError
from app.shared.schemas import PaginatedResponse
from app.shared.service import BaseService
from app.shared.utils import sanitize_filters


class AccountService(BaseService):
    def __init__(self, session):
        super().__init__(session)
        self.repo = AccountRepository(session)

    @require_permission(Resource.ACCOUNT, Action.CREATE)
    async def create(
        self, account_create: AccountCreate, current_user: User
    ) -> Account:
        return await self.repo.create(account_create)

    @require_permission(Resource.ACCOUNT, Action.UPDATE)
    async def update_plan(
        self,
        plan_update: AccountUpdatePlan,
        account_id: UUID,
        current_user: User,
    ) -> Account:
        account = await self.repo.get_one(account_id)
        if not account:
            raise NotFoundError('account')

        return await self.repo.update(
            account, {'plan': plan_update.plan.value}
        )

    @require_permission(Resource.ACCOUNT, Action.READ)
    async def show(self, account_id: UUID, current_user: User) -> Account:
        account = await self.repo.get_with_relations(account_id)

        if not account:
            raise NotFoundError('account')

        return account

    @require_permission(Resource.ACCOUNT, Action.LIST)
    async def index(
        self, filters: AccountFilters, current_user: User
    ) -> PaginatedResponse[Account]:
        clean_filters = sanitize_filters(filters)
        return await self.repo.get_many(
            filters=clean_filters, offset=filters.offset, limit=filters.limit
        )

    @require_permission(Resource.ACCOUNT, Action.ARCHIVE)
    async def archive(self, account_id: UUID, current_user: User) -> None:
        account = await self.repo.get_one(account_id)

        if not account:
            raise NotFoundError('account')

        account.archived_at = datetime.now(timezone.utc)
        await self.repo.save(account)

    @require_permission(Resource.ACCOUNT, Action.DELETE)
    async def delete(self, account_id: UUID, current_user: User) -> None:
        account = await self.repo.get_one(account_id)

        if not account:
            raise NotFoundError('account')

        await self.repo.delete(account)

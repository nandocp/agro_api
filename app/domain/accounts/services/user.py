from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.accounts.auth import (
    create_access_token,
    decode_and_validate_token,
)
from app.domain.accounts.models import PLAN_QUOTAS, User
from app.domain.accounts.repositories import (
    AccountRepository,
    RbacRepository,
    UserRepository,
)
from app.domain.accounts.schemas import (
    LoginRequest,
    UserCreate,
    UserCreateForm,
    UserFilters,
    UserRoleCreate,
)
from app.shared.authorization import require_permission
from app.shared.enums import Action, Resource
from app.shared.exceptions import (
    InvalidCredentialsError,
    NotFoundError,
    QuotaExceededError,
)
from app.shared.security import verify_password
from app.shared.service import BaseService
from app.shared.utils import sanitize_filters
from config.settings import settings


class UserService(BaseService):
    def __init__(self, session):
        super().__init__(session)
        self.repo = UserRepository(session)
        self.account_repo = AccountRepository(session)
        self.rbac_repo = RbacRepository(session)

    @require_permission(Resource.USER, Action.LIST)
    async def index(self, filters: UserFilters, current_user: User):
        clean_filters = sanitize_filters(filters)

        return await self.repo.get_many(
            filters=clean_filters, offset=filters.offset, limit=filters.limit
        )

    @require_permission(Resource.USER, Action.READ)
    async def show(self, user_id: UUID, current_user: User):
        user = await self.repo.get_with_relations(user_id)

        if not user:
            raise NotFoundError('user')

        return user

    @require_permission(Resource.USER, Action.CREATE)
    async def create(
        self, params: UserCreateForm, account_id: UUID, current_user: User
    ) -> User:
        account = await self.account_repo.get_with_relations(account_id)
        if not account:
            raise NotFoundError('account')

        if len(account.users) >= PLAN_QUOTAS[account.plan].max_users:
            raise QuotaExceededError('account.users')

        create_params = UserCreate(
            name=params.name,
            email=params.email,
            account_id=account_id,
            password=str(uuid4()),
        )

        user = await self.repo.create(create_params)
        await self.session.flush()

        rbac_params = UserRoleCreate(role=params.role, user_id=user.id)

        await self.rbac_repo.assign_role(rbac_params)

        return user

    async def login(self, login_data: LoginRequest) -> str:
        user = await self.repo.get_by_email_and_account(
            login_data.username, login_data.account_id
        )

        if not user:
            raise InvalidCredentialsError

        if user.locked_at:
            raise InvalidCredentialsError

        if not verify_password(login_data.password, user.password):
            user.failed_attempts += 1
            if user.failed_attempts >= settings.MAX_FAILED_ATTEMPTS:
                user.locked_at = datetime.now(timezone.utc)
            await self.repo.save(user)
            raise InvalidCredentialsError

        user.last_sign_in_at = user.current_sign_in_at
        user.current_sign_in_at = datetime.now(timezone.utc)
        user.failed_attempts = 0
        user.jti = uuid4()

        await self.repo.save(user)
        return create_access_token(sub=user.id, jti=user.jti)

    async def logout(self, user: User) -> None:
        user.jti = None
        await self.repo.save(user)

    async def refresh_token(self, token: str) -> str:
        sub, jti = decode_and_validate_token(token)
        user = await self.repo.get_by({'jti': jti})

        if not user or str(user.id) != sub:
            raise InvalidCredentialsError

        user.jti = uuid4()
        await self.repo.save(user)

        return create_access_token(sub=user.id, jti=user.jti)

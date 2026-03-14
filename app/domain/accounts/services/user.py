from datetime import datetime, timezone
from uuid import uuid4

from app.domain.accounts.auth import create_access_token
from app.domain.accounts.models import User
from app.domain.accounts.repositories import UserRepository
from app.domain.accounts.schemas import LoginRequest, UserCreate, UserUpdate
from app.shared.exceptions import InvalidCredentialsError
from app.shared.security import verify_password
from app.shared.service import BaseService
from config.settings import settings


class UserService(BaseService[User, UserCreate, UserUpdate]):
    def __init__(self, session):
        self.user_repo = UserRepository(User, session)
        super().__init__(User, session)

    async def login(self, login_data: LoginRequest) -> tuple[User, str]:
        user = await self.user_repo.get_by_email_and_account(
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
        token = create_access_token(sub=user.id, jti=user.jti)
        return user, token

    async def logout(self, user: User) -> None:
        user.jti = None
        await self.repo.save(user)

from datetime import datetime

from sqlalchemy.orm import Session

from agro_api.entities.core import User
from agro_api.repositories.auth import AuthRepository
from config.http_misc import unauthorized
from config.jwt import create_access_token
from config.password import verify_password


class AuthService:
    def __init__(self, session=Session | None):
        self.auth_repository = AuthRepository(model=User, session=session)

    async def login(self, form_data):
        user = await self.get_form_user(form_data)

        if not user:
            unauthorized('Incorrect email or password')

        token_data = create_access_token({'sub': str(user.id)})

        await self.login_user(user, token_data['jti'])

        return token_data['jwt']

    async def logout(self, user: User) -> True:
        user.jti = None
        return await self.auth_repository.logout(user)

    async def get_form_user(self, form_data) -> User:
        email = form_data.username
        user = await self.auth_repository.find_by_email(email)

        if not user or not verify_password(form_data.password, user.password):
            unauthorized('Incorrect email or password')

        return user

    async def login_user(self, user: User, jti: str) -> True:
        now = datetime.now()

        user.jti = jti
        user.current_sign_in_at = now
        user.last_sign_in_at = now

        return await self.auth_repository.login(user)

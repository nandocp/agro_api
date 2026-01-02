from datetime import datetime
from http import HTTPStatus

from sqlalchemy.orm import Session

from agro_api.entities.user import User
from agro_api.services.user import UserService
from config.jwt import create_access_token
from config.password import verify_password


class AuthService:
    def __init__(self, session=Session | None):
        self.session = session

    def login(self, form_data):
        user = self.get_form_user(form_data)

        if not user:
            return {
                'status_code': HTTPStatus.UNAUTHORIZED,
                'detail': 'Incorrect email or password',
            }

        token_data = create_access_token({'sub': str(user.id)})

        self.login_user(user, token_data['jti'])

        return token_data['jwt']

    def get_form_user(self, form_data) -> User:
        user = UserService(self.session).find_by_email(form_data.username)

        if not user or not verify_password(form_data.password, user.password):
            return False

        return user

    def login_user(self, user: User, jti: str):
        now = datetime.now()

        user.jti = jti
        user.current_sign_in_at = now
        user.last_sign_in_at = now

        self.session.commit()
        self.session.refresh(user)

        return True

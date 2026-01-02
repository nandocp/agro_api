from http import HTTPStatus

from agro_api.repositories.user import UserRepository
from config.jwt import create_access_token


class AuthService:
    def __init__(self, session=None):
        self.repository = UserRepository(session)

    def login(self, form_data):
        user_id = self.repository.verify_password(form_data)

        if not user_id:
            return {
                'status_code': HTTPStatus.UNAUTHORIZED,
                'detail': 'Incorrect email or password',
            }

        token_data = create_access_token({'sub': user_id})

        self.repository.login_user(form_data, token_data['jti'])

        return token_data['jwt']

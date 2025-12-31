from faker import Faker
from jwt import decode

from config.jwt import create_access_token
from config.settings import settings


def test_token_creation():
    data = {'sub': Faker().ascii_safe_email()}
    token = create_access_token(data)
    decoded = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert decoded['sub'] == data['sub']
    assert 'exp' in decoded

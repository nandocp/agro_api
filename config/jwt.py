from datetime import datetime, timedelta
from uuid import uuid6
from zoneinfo import ZoneInfo

from jwt import decode, encode

from config.settings import settings


def create_access_token(data: dict) -> str:
    payload = data.copy()
    expire = set_expiration()
    jti = generate_jti()
    payload.update({'exp': expire, 'jti': str(jti)})
    return {
        'jti': jti,
        'jwt': encode(
            payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        ),
    }


def set_expiration() -> int:
    return datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )


def generate_jti():
    return uuid6()


def decode_access_token(jwt: str) -> dict:
    return decode(jwt, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

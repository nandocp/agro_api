from datetime import datetime, timedelta, timezone

from jwt import decode, encode

from config.settings import settings


def create_access_token(sub: str, jti: str) -> str:
    now = datetime.now(timezone.utc)
    payload: dict = {
        'exp': _expiration(now),
        'iat': now,
        'jti': str(jti),
        'sub': str(sub),
    }
    return encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict:
    return decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])


def _expiration(now) -> datetime:
    return now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import uuid4
from zoneinfo import ZoneInfo

from jwt import decode, encode

from config.settings import settings


@dataclass(frozen=True)
class TokenData:
    jti: str
    jwt: str


def create_access_token(data: dict) -> TokenData:
    jti = str(uuid4())
    payload = data.copy()
    payload.update({'exp': _expiration(), 'jti': jti})
    return TokenData(
        jti=jti,
        jwt=encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM),
    )


def decode_access_token(token: str) -> dict:
    return decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])


def _expiration() -> datetime:
    return datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

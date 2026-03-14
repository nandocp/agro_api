from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from jwt import decode, encode

from config.settings import settings


@dataclass(frozen=True)
class TokenData:
    jti: str
    jwt: str


def create_access_token(data: dict) -> TokenData:
    now = datetime.now(timezone.utc)
    payload = _sanitize_data(data)
    payload.update({'exp': _expiration(now), 'iat': now})
    return TokenData(
        jti=payload['jti'],
        jwt=encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM),
    )


def decode_access_token(token: str) -> dict:
    return decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])


def _expiration(now) -> datetime:
    return now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)


def _sanitize_data(data: dict) -> dict:
    data['sub'] = str(data['sub'])
    data['jti'] = str(data['jti'])
    return data

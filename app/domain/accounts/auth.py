from datetime import datetime, timedelta, timezone

from jwt import DecodeError, ExpiredSignatureError, decode, encode

from app.shared.exceptions import AgroAPIError, InvalidCredentialsError
from config.settings import settings


def create_access_token(sub: str, jti: str) -> str:
    now = datetime.now(timezone.utc)
    payload: dict = {
        'exp': _expiration(now),
        'iat': now,
        'jti': str(jti),
        'sub': str(sub),
    }
    return encode_payload(payload)


def decode_access_token(token: str) -> dict:
    return decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])


def _expiration(now) -> datetime:
    return now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)


def encode_payload(payload: dict, secret: str = settings.SECRET_KEY) -> str:
    return encode(payload, secret, algorithm=settings.ALGORITHM)


def decode_and_validate_token(token: str) -> tuple[str, str]:
    """
    Decodes token and validates required claims.
    Returns (sub, jti) tuple.
    Raises InvalidCredentialsError or AgroAPIError on failure.
    """
    try:
        payload = decode_access_token(token)
        jti = payload.get('jti')
        sub = payload.get('sub')
        if not sub or not jti:
            raise InvalidCredentialsError
        return sub, jti
    except DecodeError:
        raise InvalidCredentialsError
    except ExpiredSignatureError:
        raise AgroAPIError(code='auth.token_expired')

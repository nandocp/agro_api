from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jwt import encode

from config.settings import settings


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = set_expiration()
    to_encode.update({'exp': expire})
    return encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

def set_expiration() -> int:
    return datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

def generate_jti():
    return

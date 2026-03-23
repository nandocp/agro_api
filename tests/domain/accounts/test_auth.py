from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest
from jwt.exceptions import InvalidSubjectError

from app.domain.accounts.auth import decode_and_validate_token, encode_payload
from app.shared.exceptions import AgroAPIError, InvalidCredentialsError


def valid_payload(**kwargs) -> dict:
    return {
        'sub': str(uuid4()),
        'jti': str(uuid4()),
        'exp': datetime.now(timezone.utc) + timedelta(hours=8),
        **kwargs,
    }


# valid token
def test_valid_token_returns_sub_and_jti():
    payload = valid_payload()
    token = encode_payload(payload)
    sub, jti = decode_and_validate_token(token)
    assert sub == payload['sub']
    assert jti == payload['jti']


# missing claims
def test_token_without_sub_raises():
    token = encode_payload(valid_payload(sub=None))
    with pytest.raises(InvalidSubjectError):
        decode_and_validate_token(token)


def test_token_without_jti_raises():
    payload = valid_payload()
    payload.pop('jti')
    token = encode_payload(payload)
    with pytest.raises(InvalidCredentialsError):
        decode_and_validate_token(token)


# invalid signature
def test_invalid_signature_raises():
    token = encode_payload(
        valid_payload(), secret='wrong_secret_test_raising_exception'
    )
    with pytest.raises(InvalidCredentialsError):
        decode_and_validate_token(token)


# malformed token
def test_malformed_token_raises():
    with pytest.raises(InvalidCredentialsError):
        decode_and_validate_token('not.a.valid.jwt')


# expired token
def test_expired_token_raises():
    token = encode_payload(
        valid_payload(exp=datetime.now(timezone.utc) - timedelta(hours=1))
    )
    with pytest.raises(AgroAPIError) as exc:
        decode_and_validate_token(token)
    assert exc.value.code == 'auth.token_expired'

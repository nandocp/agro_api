from secrets import token_hex

from config.security import hash_password, verify_password


def test_hash_password():
    password = token_hex(4)
    assert password != hash_password(password)


def test_verify_correct_password():
    password = token_hex(4)
    hashed_pwd = hash_password(password)
    assert verify_password(password, hashed_pwd)


def test_verify_incorrect_password():
    password = token_hex(4)
    incorrect_pwd = hash_password(token_hex(4))
    assert not verify_password(password, incorrect_pwd)

from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()


def hash_password(pwd: str) -> str:
    return pwd_context.hash(pwd)


def verify_password(plain_pwd: str, hashed_pwd: str) -> bool:
    return pwd_context.verify(plain_pwd, hashed_pwd)

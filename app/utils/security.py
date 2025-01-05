from datetime import datetime, timedelta

from passlib.context import CryptContext
import secrets
from typing import Union

# pwd_context = CryptContext(schemes=["bcrypt"], bcrypt__ident="2a",)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def generate_token(nbayts=None) -> str:
    '''
    :param nbayts: int
    :return: generated token "QtDuSHVd4LMDGVI2OQjlwWYh4BUtwD_A5ucVXitMjbo"
    '''
    return secrets.token_urlsafe(nbayts or 32)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_expiration_date(duration_seconds: int = 86400) -> datetime:
    return datetime.now() + timedelta(seconds=duration_seconds)

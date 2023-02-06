"""Conatin functions used to verify passwords and create access tokens."""
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

from app.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """Comapres given password in plain text with hased_password.

    Args:
        plain_password (str): password in plain text.
        hashed_password (str): encrypted password.

    Returns:
        True | False (bool): True if password are equal or False if not.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Hashes password.

    Args:
        password (str): password in plain text.

    Returns:
        (str): hashed password.
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Creates access token (JWT token).

    Args:
        data (dict): user data (email).
        expires_delta (timedelta | None, optional): token expiration time. Defaults to None.

    Returns:
        (str): access token (JWT token).
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

from typing import Union

from api import schemas

from jose import jwt
from passlib.context import CryptContext

from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def create_access_token(data: dict) -> str:
    """Create a JWT (access token) based on the provided data"""
    encoded_jwt = jwt.encode(data, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, password_digest: str) -> bool:
    """Check that hashed(plain_password) matches password_digest."""
    return pwd_context.verify(plain_password, password_digest)


def get_password_hash(password: str) -> str:
    """Return the hashed version of password"""
    return pwd_context.hash(password)


def decode_token(token: str) -> Union[schemas.Token, None]:
    """Return a dictionary that represents the decoded JWT."""
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    return schemas.Token(**decoded) if decoded.get("sub") else None

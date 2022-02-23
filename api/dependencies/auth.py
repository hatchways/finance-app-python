from api.core import security
from api.core.exceptions import CredentialsException
from api.crud.user import UserCrud
from api.dependencies.db import get_db
from fastapi import Depends
from fastapi.security.utils import get_authorization_scheme_param
from jose import ExpiredSignatureError, JWTError
from sqlalchemy.orm.session import Session
from starlette.requests import Request


def get_token(request: Request):
    header_authorization = request.headers.get("Authorization")
    scheme, header_param = get_authorization_scheme_param(header_authorization)
    if scheme != "Bearer":
        raise CredentialsException
    return header_param


def get_current_user(token: str = Depends(get_token), db: Session = Depends(get_db)):
    """Decode the provided jwt and extract the user using the [sub] field."""
    if not token:
        return None
    try:
        payload = security.decode_token(token)
        if not payload:
            raise CredentialsException
        email = payload.sub
        if email is None:
            # Something wrong with the token
            raise CredentialsException
        # Get user from database
        user = UserCrud.get_user_by_email(db, email)
        if user is None:
            raise CredentialsException
        return user
    except (JWTError, ExpiredSignatureError):
        # Something wrong with the token
        raise CredentialsException

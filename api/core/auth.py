from typing import Union

from api.core import security
from api.crud import UserCrud
from api.models import User
from sqlalchemy.orm import Session


async def login_user(db: Session, email: str, password: str) -> Union[bool, User]:
    """Based on the provided email & password, verify that the credentials match
    the records contained in the database.
    """
    user = UserCrud.get_user_by_email(db, email)
    if not user:
        # No user with that email exists in the database
        return False
    if not security.verify_password(password, user.password_digest):
        # The user exists but the password was incorrect
        return False
    return user

from typing import Union

from api import schemas
from api.core import security
from api.models import User
from pydantic.networks import EmailStr
from sqlalchemy.orm.session import Session


class UserCrud:
    @classmethod
    def get_user_by_email(cls, db: Session, email: EmailStr) -> Union[User, None]:
        """Get a single user by email"""
        return db.query(User).filter(User.email == email.lower()).one_or_none()

    @classmethod
    def create_user(cls, db: Session, data: schemas.UserCreate) -> User:
        """Create a user"""
        user = User(
            email=data.email.lower(),
            password_digest=security.get_password_hash(data.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

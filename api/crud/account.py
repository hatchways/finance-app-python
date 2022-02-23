from typing import List

from api.models import Account
from sqlalchemy.orm.session import Session


class AccountCrud:
    @classmethod
    def get_accounts(cls, db: Session, user_id: int) -> List[Account]:
        """
        Get all accounts for a given user.

        Args:
            db (Session)
            user_id (int)

        Returns:
            List[Account]:
        """
        res = db.query(Account).filter(Account.user_id == user_id).all()
        return res

from datetime import datetime
from typing import List

from api.models import Transaction
from sqlalchemy.orm.session import Session


class TransactionCrud:
    @classmethod
    def get_transactions_for_range(
        cls,
        db: Session,
        user_id: int,
        start_date: datetime,
        end_date: datetime,
    ) -> List[Transaction]:
        """
        Get all transactions between start_date and end_date

        Args:
            db (Session)
            user_id (int)
            start_date (datetime)
            end_date (datetime)

        Returns:
            List[Transaction]
        """

        return (
            db.query(Transaction)
            .filter(
                Transaction.user_id == user_id,
                Transaction.date >= start_date,
                Transaction.date <= end_date,
            )
            .all()
        )

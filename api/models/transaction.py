from decimal import Decimal

from api.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import (
    Boolean,
    DateTime,
    Integer,
    Numeric,
    String,
)


class Transaction(Base):
    """Transaction Table"""

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    plaid_transaction_id = Column(String, unique=True, index=True, nullable=False)
    plaid_category_id = Column(String)
    categories = Column(String)  # comma delimited
    type = Column(String, nullable=False)
    name = Column(String, nullable=False)
    amount_str = Column(String, nullable=False)
    iso_currency_code = Column(String)
    unofficial_currency_code = Column(String)
    date = Column(DateTime(timezone=True))
    pending = Column(Boolean)

    account = relationship(
        "Account", back_populates="transactions", foreign_keys=[account_id]
    )
    user = relationship("User", back_populates="transactions", foreign_keys=[user_id])

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"{self.id}"

    @property
    def amount(self) -> Decimal:
        """
        The amount as a Decimal. A positive value represents money being added to the
        account. A negative value represents money being deducted from the account.

        Returns:
            Decimal
        """
        return Decimal(self.amount_str)

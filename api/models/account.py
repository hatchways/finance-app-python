from decimal import Decimal

from api.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Integer, Numeric, String


class Account(Base):
    """Account Table"""

    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    plaid_account_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    mask = Column(String, nullable=False)
    official_name = Column(String)
    current_balance_str = Column(String, nullable=False)
    iso_currency_code = Column(String)
    unofficial_currency_code = Column(String)
    account_type = Column(String, nullable=False)
    account_subtype = Column(String, nullable=False)

    user = relationship("User", back_populates="accounts", foreign_keys=[user_id])
    transactions = relationship("Transaction", back_populates="account")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"{self.id}"

    @property
    def current_balance(self):
        return Decimal(self.current_balance_str)

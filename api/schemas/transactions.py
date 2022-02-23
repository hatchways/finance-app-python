from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class Transaction(BaseModel):
    """One-to-one representation of the SQLAlchemy Transaction model"""

    id: int
    account_id: int
    categories: str  # comma delimited
    amount: Decimal
    date: datetime
    iso_currency_code: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

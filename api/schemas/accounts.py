from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class Account(BaseModel):
    """One-to-one representation of the SQLAlchemy Accounts model"""

    id: int
    name: str
    current_balance: Decimal
    available_balance: Decimal
    iso_currency_code: str
    account_type: str
    account_subtype: str

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

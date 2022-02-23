from api.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import DateTime, Integer, String


class User(Base):
    """User Table"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_digest = Column(String, unique=True, index=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    accounts = relationship("Account", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")

    def __repr__(self):
        return f"{self.id} | {self.email}"

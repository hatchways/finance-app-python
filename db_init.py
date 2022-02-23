from typing import List

from api.database import Base, engine
from api.models import Account, Transaction, User
from sqlalchemy import MetaData
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.sql.schema import Table

if __name__ == "__main__":
    metadata: MetaData = Base.metadata
    reversed_tables: List[Table] = [
        Transaction.__table__,
        Account.__table__,
        User.__table__,
    ]
    try:
        print("-- Dropping All Tables --")
        for t in reversed_tables:
            print(f"...{t.name}")
        Base.metadata.drop_all(bind=engine, tables=reversed_tables)
    except ProgrammingError:
        pass

    print("\n-- Creating Tables --")
    metadata: MetaData = Base.metadata
    metadata.create_all(bind=engine)
    # Note: order of table creation depends on import order in api/models/__init__.py
    for t in metadata.tables:
        print(f"...{t}")
    print("\n")

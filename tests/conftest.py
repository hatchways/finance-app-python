import os
from typing import Generator

import pytest
from api.database import Base
from api.dependencies.db import get_db
from fastapi.testclient import TestClient
from main import app
from seed import seed_data
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

engine = create_engine(os.environ["DATABASE_TEST_URL"])
TestingSessionLocal = sessionmaker(autoflush=False, bind=engine)
Base.metadata.create_all(engine)


def override_get_db() -> Generator:
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True, scope="session")
def prepare_once():
    """Runs only one time before the first test"""
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client() -> TestClient:
    """Return the main test client"""
    test_client = TestClient(app)
    app.dependency_overrides[get_db] = override_get_db
    return test_client


@pytest.fixture(autouse=True, scope="function")
def reset_db():
    """Reset the database before each test"""
    Base.metadata.create_all(bind=engine)
    (yield)
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def seed_db():
    db = TestingSessionLocal()
    seed_data(db)
    db.close()


@pytest.fixture(scope="function")
def db() -> Session:
    """Return a session"""
    _db = next(override_get_db())
    (yield _db)
    _db.close()

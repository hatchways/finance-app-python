import json

from api.core.security import get_password_hash
from api.models import User
from fastapi.testclient import TestClient
from sqlalchemy.orm.session import Session


def test_signup(db: Session, client: TestClient):
    response = client.post(
        "/api/signup",
        headers={"Content-Type": "application/json"},
        data=(json.dumps({"email": "test@test.com", "password": "sample"})),
    )
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["token"] is not None
    assert response_body["user"]["email"] == "test@test.com"

    db_user = db.query(User).filter(User.email == "test@test.com").one_or_none()
    assert db_user is not None


def test_signup_duplicate_user(db: Session, client: TestClient):
    user = User(email="test@test.com", password_digest=(get_password_hash("sample")))
    db.add(user)
    db.commit()
    response = client.post(
        "/api/signup",
        headers={"Content-Type": "application/json"},
        data=(json.dumps({"email": "test@test.com", "password": "sample"})),
    )

    assert response.status_code == 400

from api.core.security import create_access_token
from fastapi.testclient import TestClient


def test_get_authenticated_user(client: TestClient, seed_db: None):
    token = create_access_token(data={"sub": "test@test.com"})
    response = client.get(
        "/api/user",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )
    assert response.status_code == 200

    response_body = response.json()
    assert response_body["email"] == "test@test.com"
    assert response_body["id"]
    assert response_body["created_at"]
    assert response_body["updated_at"]

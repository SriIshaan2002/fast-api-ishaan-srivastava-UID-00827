from fastapi.testclient import TestClient

from app.main import app
from app.models.model import User

client = TestClient(app)
mock_user = {
    "username": "Tester",
    "mobile": "1234567890",
    "email": "TestUser@Example.com",
    "password": "SecurePassword123!",
}


def test_signup_successful():
    """Test that a user can successfully register with valid details."""
    response = client.post("/auth/signup", json=mock_user)
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert "user_uuid" in data


def test_signup_missing_password():
    """Test that missing required fields triggers a 420/400 validation error."""
    response = client.post("/auth/signup", json={"email": "missing@test.com"})
    assert response.status_code == 422


def test_signup_invalid_email_format():
    """Test that an improperly formatted email address is rejected."""
    bad_user = {"email": "notanemail", "password": "Password123!"}
    response = client.post("/auth/signup", json=bad_user)
    assert response.status_code in [400, 422]


def test_login_successful():
    """Test logging in with matching credentials returns an access token."""
    login_payload = {
        "email": mock_user["email"].lower(),
        "password": mock_user["password"],
    }
    response = client.post("/auth/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


def test_login_wrong_password():
    """Test that an incorrect password returns a 401 Unauthorized error."""
    invalid_payload = {"email": mock_user["email"], "password": "WrongPassword!!!"}
    response = client.post("/auth/login", json=invalid_payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"

async def delete_user():
    user = await User.get_or_none(email=mock_user["email"])
    if user:
        user.delete()

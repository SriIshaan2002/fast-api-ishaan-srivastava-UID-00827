import pytest
from httpx import AsyncClient

from app.auth import jwt_handler

pytestmark = pytest.mark.asyncio


async def test_signup(client: AsyncClient):
    response = await client.post(
        "/auth/signup",
        json={
            "username": "Ishaan",
            "password": "password",
            "email": "test@example.com",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert "user_uuid" in data


async def test_signup_same_email(client: AsyncClient):
    user = {
        "email": "test_dup@example.com",
        "password": "password",
        "username": "Ishaan",
    }
    await client.post("/auth/signup", json=user)
    response = await client.post("/auth/signup", json=user)

    assert response.status_code == 400


async def test_login(client: AsyncClient):
    user = {
        "email": "test_login@example.com",
        "password": "password",
        "username": "Ishaan",
    }

    await client.post("/auth/signup", json=user)

    response = await client.post("/auth/login", json=user)
    assert response.status_code == 200


async def test_login_wrong(client: AsyncClient):
    user = {
        "email": "test_wrong@example.com",
        "password": "password",
        "username": "Ishaan",
    }

    await client.post("/auth/signup", json=user)

    response = await client.post(
        "/auth/login",
        json={
            "email": "test_wrong@example.com",
            "password": "wrong",
            "username": "Ishaan",
        },
    )
    assert response.status_code == 401


async def test_refresh(client: AsyncClient):
    token = await client.post(
        "/auth/signup",
        json={
            "email": "test_refresh@example.com",
            "password": "password",
            "username": "Ishaan",
        },
    )

    access_token = token.json()["access_token"]
    payload = jwt_handler.decode_and_verify_token(access_token)
    refresh_token = token.json()["user_uuid"]
    user_id = payload.user_id

    response = await client.post(
        "/auth/refresh",
        params={"auth_uuid": str(refresh_token), "user_id": str(user_id)},
    )
    assert response.status_code == 200

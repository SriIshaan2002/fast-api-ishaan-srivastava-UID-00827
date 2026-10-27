"""
This module defines the authentication routes for user signup and login.
It uses JWT for token-based authentication.
The routes handle user creation, login, token generation, refresh, and logout.
"""

from fastapi import APIRouter, HTTPException, status

from app.exception import (
    CustomBaseException,
)
from app.schemas.token import TokenResponse
from app.schemas.user import UserCreate, UserLogin
from app.service.authService import AuthService


authRouter = APIRouter(prefix="/auth", tags=["Authentication"])


@authRouter.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=TokenResponse,
)
async def signup(user: UserCreate):
    """
    Registers a new user and generates access and refresh tokens.
    """
    try:
        return await AuthService.signup(user)
    except CustomBaseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@authRouter.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=TokenResponse,
)
async def login(user: UserLogin):
    """
    Authenticates a user and generates access and refresh tokens.
    """
    try:
        return await AuthService.login(user)
    except CustomBaseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@authRouter.get("/refresh", status_code=status.HTTP_200_OK)
async def refresh(auth_uuid: str):
    """
    Validates a refresh token and generates a new access token.
    """
    try:
        return await AuthService.refresh(auth_uuid)
    except CustomBaseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@authRouter.post("/logout", status_code=status.HTTP_200_OK)
async def logout(auth_uuid: str):
    """
    Invalidates a refresh-token session by revoking its database record.
    """
    try:
        return await AuthService.logout(auth_uuid=auth_uuid)
    except CustomBaseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@authRouter.post(
    "/reactivate", status_code=status.HTTP_200_OK, response_model=TokenResponse
)
async def reactivate(user: UserLogin):
    """
    This is a reactivating api for inactive users
    """
    try:
        return await AuthService.reactivate(user)
    except CustomBaseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

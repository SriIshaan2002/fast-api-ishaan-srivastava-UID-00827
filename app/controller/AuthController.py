"""
Authentication routes for user registration, login, token refresh, logout,
and account reactivation.

This module exposes authentication endpoints and delegates business logic
to AuthService. Custom application exceptions are converted into
FastAPI HTTP exceptions with the corresponding status codes.
"""

from fastapi import HTTPException, status

from app.exception import CustomBaseException
from app.schemas.token import TokenResponse
from app.schemas.user import UserCreate, UserLogin
from app.service.authService import AuthService
from app.routes.AuthRouter import authRouter

@authRouter.post(
    "/signup", status_code=status.HTTP_201_CREATED, response_model=TokenResponse
)
async def signup(user: UserCreate) -> TokenResponse:
    """
    Register a new user and generate authentication tokens.

    Args:
        user (UserCreate): User registration details.

    Returns:
        TokenResponse: Access and refresh tokens for the registered user.

    Raises:
        HTTPException: If registration fails due to an application error.
    """
    try:
        return await AuthService.signup(user)
    except CustomBaseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e


@authRouter.post("/login", status_code=status.HTTP_200_OK, response_model=TokenResponse)
async def login(user: UserLogin) -> TokenResponse:
    """
    Authenticate a user and generate authentication tokens.

    Args:
        user (UserLogin): User login credentials.

    Returns:
        TokenResponse: Access and refresh tokens for the authenticated user.

    Raises:
        HTTPException: If authentication fails due to an application error.
    """
    try:
        return await AuthService.login(user)
    except CustomBaseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e


@authRouter.post("/refresh")
async def refresh(auth_uuid: str, user_id: int) -> dict:
    """
    Refresh the access token for an existing user session.

    Args:
        auth_uuid (str): UUID identifying the refresh-token session.

    Returns:
        dict: A response containing the newly generated access token.

    Raises:
        HTTPException: If the token is invalid or the refresh operation fails.
    """
    try:
        return await AuthService.refresh(auth_uuid, user_id=user_id)
    except CustomBaseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e


@authRouter.post("/logout", status_code=status.HTTP_200_OK)
async def logout(auth_uuid: str) -> dict:
    """
    Invalidate a user session.

    Args:
        auth_uuid (str): UUID identifying the session to invalidate.

    Returns:
        dict: A response indicating the result of the logout operation.

    Raises:
        HTTPException: If the session cannot be invalidated.
    """
    try:
        return await AuthService.logout(auth_uuid=auth_uuid)
    except CustomBaseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e


@authRouter.post(
    "/reactivate", status_code=status.HTTP_200_OK, response_model=TokenResponse
)
async def reactivate(user: UserLogin) -> TokenResponse:
    """
    Reactivate an inactive user account and generate authentication tokens.

    Args:
        user (UserLogin): User credentials used to verify the account.

    Returns:
        TokenResponse: Access and refresh tokens for the reactivated user.

    Raises:
        HTTPException: If reactivation fails due to an application error.
    """
    try:
        return await AuthService.reactivate(user)
    except CustomBaseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e


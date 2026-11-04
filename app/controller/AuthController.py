"""
Authentication routes for user registration, login, token refresh, logout,
and account reactivation.

This module exposes authentication endpoints and delegates business logic
to AuthService. Custom application exceptions are converted into
FastAPI HTTP exceptions with the corresponding status codes.
"""

from fastapi import status

from app.exception import CustomBaseException
from app.routes.AuthRouter import authRouter
from app.schemas.token import TokenResponse
from app.schemas.user import UserCreate, UserLogin
from app.service.authService import AuthService


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
        raise e


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
        raise e


@authRouter.post("/refresh")
async def refresh(refresh_token: str) -> dict:
    """
    Refresh the access token for an existing user session.

    Args:
        refresh_token (str): The refresh token for the session.

    Returns:
        dict: A response containing the newly generated access token.

    Raises:
        HTTPException: If the token is invalid or the refresh operation fails.
    """
    try:
        return await AuthService.refresh(refresh_token)
    except CustomBaseException as e:
        raise e


@authRouter.post("/logout", status_code=status.HTTP_200_OK)
async def logout(refresh_token: str) -> dict:
    """
    Invalidate a user session.

    Args:
        refresh_token (str): The refresh token for the session.

    Returns:
        dict: A response indicating the result of the logout operation.

    Raises:
        HTTPException: If the session cannot be invalidated.
    """
    try:
        return await AuthService.logout(refresh_token=refresh_token)
    except CustomBaseException as e:
        raise e


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
        raise e

"""
This module provides dependency functions to
authenticate and extract the active user from requests.
"""

from typing import Annotated

import jwt
from fastapi import Header, HTTPException, status

from app.auth.jwt_handler import TokenPayload
from app.auth.jwt_handler import decode_and_verify_token as decode
from app.models.model import User
from constants import AUTH_ERRORS


async def get_active_user(x_custom_token: Annotated[str, Header()]) -> User:
    """Extract and validate the currently authenticated
    active user using the custom JWT header.

    Args:
        x_custom_token (str): The incoming raw JSON
        Web Token supplied in the 'X-Custom-Token' header.

    Returns:
        User: The active and verified Tortoise ORM User model instance.

    Raises:
        HTTPException: 401 error if the token is
        expired, structurally invalid, or matching no user.
        HTTPException: 403 error if the verified
        user exists but their account is marked inactive.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=AUTH_ERRORS.invalid_credentials,
    )

    try:
        payload: TokenPayload = decode(x_custom_token)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        raise credentials_exception

    current_user: User | None = await User.get_or_none(id=payload.user_id)

    if current_user is None:
        raise credentials_exception

    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive"
        )
    return current_user

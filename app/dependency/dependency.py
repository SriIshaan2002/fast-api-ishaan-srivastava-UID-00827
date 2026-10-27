"""
File to get the current signed in user details
"""
from typing import Annotated

import jwt
from fastapi import Header, HTTPException, status

from app.auth.jwt_handler import TokenPayload
from app.auth.jwt_handler import decode_and_verify_token as decode
from app.models.model import User
from constants import AUTH_ERRORS
import jwt

async def get_active_user(x_custom_token: Annotated[str, Header()]) -> User:
    """
    Gets the user details by analysing the incomming JWT token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=AUTH_ERRORS.invalid_credentials,
    )
    try:
        payload: TokenPayload = decode(
            x_custom_token,
        )
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        raise credentials_exception
    current_user: User | None = await User.get_or_none(id=payload.user_id)
    if current_user is None or not current_user.is_active:
        raise credentials_exception
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive"
        )
    return current_user

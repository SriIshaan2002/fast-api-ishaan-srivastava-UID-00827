"""
file to add middleware, implementing RBAC on Admins, Users
"""

import jwt
from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.auth.jwt_handler import TokenPayload, decode_and_verify_token
from app.models import User
from constants import AUTH_ERRORS


async def unified_auth_middleware(request: Request, call_next):
    """
    Protecting the non public endpoints
    """
    path = request.url.path
    if (
        path.startswith("/auth")
        or path.startswith("/docs")
        or path.startswith("/openapi")
    ):
        return await call_next(request)
    x_custom_token = request.headers.get("x-custom-token")
    if not x_custom_token:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": AUTH_ERRORS.invalid_token},
        )
    try:
        payload: TokenPayload = decode_and_verify_token(x_custom_token)
        current_user = await User.get_or_none(id=payload.user_id)
        if current_user is None or not current_user.is_active:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": AUTH_ERRORS.invalid_token},
            )
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": AUTH_ERRORS.invalid_token},
        )
    if path.startswith("/admin"):
        if not current_user.is_admin:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": AUTH_ERRORS.invalid_credentials},
            )

    if path.startswith("/owners"):
        if not (payload.is_owner or payload.is_admin):
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": AUTH_ERRORS.invalid_credentials},
            )

    if path.startswith("/owners"):
        if not (payload.is_owner or payload.is_admin):
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": AUTH_ERRORS.invalid_credentials},
            )

    if path.startswith("/owners"):
        if not (payload.is_owner or payload.is_admin):
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": AUTH_ERRORS.invalid_credentials},
            )
    request.state.user = current_user
    return await call_next(request)

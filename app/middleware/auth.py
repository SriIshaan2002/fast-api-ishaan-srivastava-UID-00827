"""
This module provides unified authentication and Role-Based
Access Control (RBAC) middleware for intercepting incoming HTTP requests.
"""

import jwt
from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.auth.jwt_handler import TokenPayload, decode_and_verify_token
from app.models import User
from constants import AUTH_ERRORS


async def unified_auth_middleware(request: Request, call_next):
    """Intercept HTTP requests to enforce route protection,
    token validation, and Role-Based Access Control (RBAC).

    This middleware bypasses public routes
    (/auth, /docs, /openapi) and checks all other paths
    for a valid 'X-Custom-Token' header.
    It validates the user session status and restricts access
    to /admin and /owners routes based on the derived user roles.

    Args:
        request (Request): The incoming FastAPI/Starlette
        request context layer object.
        call_next (Callable): The next downstream request
        handler or endpoint processing controller.

    Returns:
        Response: A standard FastAPI Response/JSONResponse
        stream depending on the outcome of authorization checks.
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
    request.state.user = current_user
    return await call_next(request)

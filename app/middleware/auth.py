"""
file to add middleware, implementing RBAC on Admins, Users
"""
import jwt
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.models import User
from app.auth.jwt_handler import decode_and_verify_token, TokenPayload
import constants as const

app = FastAPI()

@app.middleware("http")
async def unified_auth_middleware(request: Request, call_next):
    """
    Protecting the non public endpoints
    """
    path = request.url.path
    if path.startswith("/auth"):
        return await call_next(request)
    x_custom_token = request.headers.get("x-custom-token")
    if not x_custom_token:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": const.INVALID_TOKEN}
        )
    try:
        payload: TokenPayload = decode_and_verify_token(x_custom_token)
        current_user = await User.get_or_none(id=payload.user_id)            
        if current_user is None or not current_user.is_active:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": const.INVALID_TOKEN}
            )
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": const.INVALID_TOKEN}
        )
    if path.startswith("/admin"):
        if not current_user.is_admin:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": const.ACCESS_FORBIDDEN_ADMIN}
            )

    if path.startswith("/owners"):
        if not payload.is_owner:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": const.ACCESS_FORBIDDEN_ADMIN}
            )
    request.state.user = current_user
    return await call_next(request)

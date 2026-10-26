from fastapi import Depends, HTTPException, Header, status
from typing import Annotated
from app.models.model import User 
from app.auth.jwt_handler import decode_and_verify_token as decode
from app.auth.jwt_handler import TokenPayload
import constants as const
import jwt

async def get_active_user(x_custom_token: Annotated[str, Header()]) -> User:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=const.INVALID_TOKEN,)
    try:
        payload: TokenPayload = decode(x_custom_token,)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        raise credentials_exception
    current_user: User | None = await User.get_or_none(id=payload.user_id)
    if current_user is None or not current_user.is_active:
        raise credentials_exception
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive")
    return current_user

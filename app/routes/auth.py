"""
This module defines the authentication routes for user signup and login.
It uses JWT for token-based authentication.
The routes handle user creation, login, and token generation.
"""

from fastapi import APIRouter, HTTPException, status

import constants as const
from app.auth import jwt_handler
from app.models import Owner, Token, User
from app.schemas.token import TokenResponse
from app.schemas.user import UserCreate, UserLogin

authRouter = APIRouter(prefix="/auth", tags=["Authentication"])


@authRouter.post(
    "/signup", status_code=status.HTTP_201_CREATED, response_model=TokenResponse
)
async def signup(user: UserCreate):
    """
    This is a Sign-up API for users.
    """
    user_exists = await User.filter(email=user.email).exists()
    if user_exists:
        raise HTTPException(status_code=400, detail=const.REGISTERED_EMAIL)
    user.email = user.email.lower()
    created_user = await User.create(**user.model_dump())
    access_token = jwt_handler.create_access_token(
        user_id=created_user.id,
        username=created_user.username,
        is_admin=False,
        is_owner=False,
    )
    refresh_token, token_uuid = jwt_handler.create_refresh_token(
        user_id=created_user.id,
        username=created_user.username,
        is_admin=False,
        is_owner=False,
    )
    await Token.create(user_id=created_user.id, uuid=token_uuid, token=refresh_token)
    return TokenResponse(access_token=access_token, user_uuid=str(token_uuid))


@authRouter.post("/login", status_code=status.HTTP_200_OK, response_model=TokenResponse)
async def login(user: UserLogin):
    """
    This is a login api for users
    """
    existing_user = await User.filter(email=user.email).first()
    if existing_user.password != user.password:
        raise HTTPException(status_code=401, detail=const.INVALID_PASSWORD)
    if not existing_user:
        raise HTTPException(status_code=404, detail=const.USER_NOT_FOUND)
    access_token = jwt_handler.create_access_token(
        user_id=existing_user.id,
        username=existing_user.username,
        is_admin=False,
        is_owner=False,
    )
    refresh_token, token_uuid = jwt_handler.create_refresh_token(
        user_id=existing_user.id,
        username=existing_user.username,
        is_admin=False,
        is_owner=False,
    )
    await Token.create(user_id=existing_user.id, uuid=token_uuid, token=refresh_token)
    return TokenResponse(access_token=access_token, user_uuid=str(token_uuid))


@authRouter.get("/refresh")
async def refresh(auth_uuid: str):
    """
    This is a refresh token api which returns a JWT token
    """
    existing_token = await Token.filter(uuid=auth_uuid).first()
    if not existing_token or existing_token.revoked_at is not None:
        raise HTTPException(status_code=401, detail=const.INVALID_TOKEN)
    payload = jwt_handler.decode_and_verify_token(existing_token.token)
    if not payload:
        raise HTTPException(status_code=401, detail=const.INVALID_TOKEN)
    user = await User.filter(id=existing_token.id).first()
    if not user:
        raise HTTPException(status_code=404, detail=const.USER_INACTIVE)
    is_owner = await Owner.filter(user_id=user.id).exists()
    access_token = jwt_handler.create_access_token(
        user_id=user.id,
        username=user.username,
        is_admin=user.is_admin,
        is_owner=is_owner,
    )
    return {const.ACCESS_TOKEN: access_token}


@authRouter.post("/logout", status_code=status.HTTP_200_OK)
async def logout(auth_uuid: str):
    """
    Invalidates a user session by deleting the matching JWT tracking UUID
    from the database using Tortoise ORM.
    """
    deleted_count = await Token.filter(auth_uuid=auth_uuid).delete()
    if deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session already logged out or invalid UUID.",
        )
    return {"detail": const.LOGGED_OUT}

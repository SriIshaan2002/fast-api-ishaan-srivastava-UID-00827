"""
1.MODULE DOCSTRING
   --------------------------------------------------
Creating all the apis related to user management and authentication.
2.IMPORTS
   --------------------------------------------------

"""
from fastapi import APIRouter, HTTPException

from constants import GENERAL, AUTH_ERRORS, SUCCESS_MESSAGES
from app.models import User
from app.schemas import UserCreate, UserResponse

import constants as const
from app.models import User
from app.schemas import UserCreate, UserUpdate, UserResponse
from fastapi import APIRouter, HTTPException, Header, status
from typing import Annotated 
from app.auth import jwt_handler as jwt
from app.auth import TokenPayload
from app.dependency.dependency import get_active_user
from fastapi import Depends


routerAdmin = APIRouter(tags=["User Management ADMIN"], prefix="/admin")
routerUser = APIRouter(tags=["User Management"], prefix="/users")


@routerAdmin.get("/")
async def get_users():
    """
    Get all users
    """
    users = await User.all()
    return users

@routerAdmin.get("/{user_id}")
async def get_user(user_id: int):
    """
    Get a user by ID
    """
    user = await User.get_or_none(user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail=AUTH_ERRORS.user_not_found)
    return user

@routerAdmin.post("/")
async def create_user(user: UserCreate):
    """
    Create a new user
    """
    user = await User.create(**user.dict())
    return UserResponse.from_orm(user)

@routerAdmin.get("/{email}")
async def get_user_by_email(email: str):
    """
    Get a user by email
    """
    user = await User.get_or_none(email=email)
    if not user:
        raise HTTPException(status_code=404, detail=AUTH_ERRORS.user_not_found)
    return UserResponse.from_orm(user)

@routerAdmin.delete("/{user_id}")
async def delete_user(user_id: int, current_user = Depends(get_active_user)):
    """
    Delete a user by ID
    """
    user = await User.get_or_none(id=user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=404, detail=AUTH_ERRORS.user_not_found)
    await user.update_from_dict({"is_active": False, "updated_by_id" : current_user.id}).save()
    return {"message": SUCCESS_MESSAGES.user_deleted}

@routerAdmin.put("/users/{user_id}/role")
async def update_user_admin_status(
    user_id: int, 
    admin_change: bool, 
    current_user: User = Depends(get_active_user)
):
    """
    Admin only: Update a specific user's is_admin status by their ID path parameter.
    """
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete same user"
        )
    target_user = await User.get_or_none(id=user_id)
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=AUTH_ERRORS.user_not_found)
    target_user.is_admin = admin_change
    await target_user.save()
    return {
        "status": "success",
        "message": const.STATUS_UPDATE
    }

@routerUser.put("/")
async def update_user(user: UserUpdate, current_user: User = Depends(get_active_user)):
    """
    Update a user by ID
    """
    update_data = user.model_dump(exclude_unset=True) 
    current_user.update_from_dict(update_data)
    await current_user.save()
    return UserResponse.model_validate(current_user)


@routerUser.get("/profile")
async def get_profile(current_user: User = Depends(get_active_user)):
    """
    Getting the current user profile with the help of jwt token
    """
    return UserResponse.from_orm(current_user)

@routerUser.delete("/")
async def deactivate_my_account(current_user: User = Depends(get_active_user)):
    """
    Self-deactivation / soft delete by the user with the help of jwt token
    """
    current_user.is_active = False
    current_user.updated_by = current_user.id
    await current_user.save()
    return {"message":SUCCESS_MESSAGES.user_deleted}

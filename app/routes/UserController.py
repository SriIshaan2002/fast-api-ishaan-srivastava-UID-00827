"""
1.MODULE DOCSTRING
   --------------------------------------------------
Creating all the apis related to user management and authentication.
2.IMPORTS
   --------------------------------------------------

"""
from app.models import User
from fastapi import APIRouter, HTTPException
from app.schemas import UserCreate, UserUpdate, UserResponse
import constants as const

routerAdmin = APIRouter(tags=["User Management ADMIN"], prefix="/users")
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
        raise HTTPException(status_code=404, detail=const.USER_NOT_FOUND)
    return user

@routerUser.post("/")
async def create_user(user: UserCreate):
    """
    Create a new user
    """
    user = await User.create(**user.dict())
    return UserResponse.from_orm(user)

@routerUser.get("/{email}")
async def get_user_by_email(email: str):
    """
    Get a user by email
    """
    user = await User.get_or_none(email=email)
    if not user:
        raise HTTPException(status_code=404, detail=const.USER_NOT_FOUND)
    return UserResponse.from_orm(user)

@routerUser.delete("/{user_id}")
async def delete_user(user_id: int):
    """
    Delete a user by ID
    """
    user = await User.get_or_none(user_id=user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=404, detail=const.USER_NOT_FOUND)
    await user.update_from_dict({"is_active": False}).save()
    return {"message": const.USER_DELETED}

@routerUser.put("/{user_id}")
async def update_user(user_id: int, user: UserUpdate):
    """
    Update a user by ID
    """
    existing_user = await User.get_or_none(user_id=user_id)
    if not existing_user or not existing_user.is_active :
        raise HTTPException(status_code=404, detail=const.USER_NOT_FOUND)
    await existing_user.update_from_dict(user.dict()).save()
    return UserResponse.from_orm(existing_user)

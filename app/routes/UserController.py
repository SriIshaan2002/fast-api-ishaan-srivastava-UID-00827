"""
This module defines APIs for user management and authentication-related
user operations.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependency.dependency import get_active_user
from app.models import User
from app.schemas import UserCreate, UserResponse, UserUpdate
from app.service.UserService import UserService


async def require_admin(current_user: User = Depends(get_active_user)) -> User:
    """Allow access only to authenticated administrators."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator privileges required",
        )
    return current_user


routerAdmin = APIRouter(
    prefix="/admin",
    tags=["User Management ADMIN"],
    dependencies=[Depends(require_admin)],
)
routerUser = APIRouter(
    prefix="/users",
    tags=["User Management"],
    dependencies=[Depends(get_active_user)],
)


@routerAdmin.get("/", response_model=list[UserResponse])
async def get_users():
    """Retrieve all users."""
    return await UserService.get_all_users()

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
    """Retrieve a user by email address."""
    return await UserService.get_user_by_email(email)


@routerAdmin.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Retrieve a user by ID."""
    return await UserService.get_user(user_id)


@routerAdmin.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate):
    """Create a new user."""
    return await UserService.create_user(data)


@routerAdmin.delete("/{user_id}")
async def delete_user(user_id: int, current_user: User = Depends(get_active_user)):
    """Soft-delete a user by ID."""
    user = await UserService.get_user(user_id)
    return await UserService.deactivate_user(
        user=user,
        updated_by_id=current_user.id,
    )


@routerUser.put("/", response_model=UserResponse)
async def update_user(data: UserUpdate, current_user: User = Depends(get_active_user)):
    """Update the authenticated user's profile."""
    return await UserService.update_user(
        user=current_user,
        data=data,
    )


@routerUser.get("/profile", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_active_user)):
    """Retrieve the authenticated user's profile."""
    return current_user


@routerUser.delete("/")
async def deactivate_my_account(current_user: User = Depends(get_active_user)):
    """Deactivate the authenticated user's account."""
    return await UserService.deactivate_user(
        user=current_user,
        updated_by_id=current_user.id,
    )

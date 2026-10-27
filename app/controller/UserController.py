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
    """Allow access only to authenticated administrators.

    Args:
        current_user (User): The active authenticated
        User instance from dependency injection.

    Returns:
        User: The authenticated administrator instance.

    Raises:
        HTTPException: 403 error if the
        authenticated user lacks admin privileges.
    """
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
    """Retrieve all users in the system.

    Returns:
        list[UserResponse]: A list containing
        serialized representations of all user records.
    """
    return await UserService.get_all_users()

async def get_user_by_email(email: str):
    """Retrieve a single user using their email address.

    Args:
        email (str): The specific target email address to look up.

    Returns:
        User: The database User instance matching the target email.
    """
    return await UserService.get_user_by_email(email)


@routerAdmin.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Retrieve a single user record by their unique integer ID.

    Args:
        user_id (int): The database primary
        key identifier of the targeted user.

    Returns:
        UserResponse: The serialized data of the requested user.
    """
    return await UserService.get_user(user_id)


@routerAdmin.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate):
    """Create and persist a new user record in the system.

    Args:
        data (UserCreate): Validated Pydantic
        schema containing initial user fields.

    Returns:
        UserResponse: The serialized entry of the newly generated user profile.
    """
    return await UserService.create_user(data)


@routerAdmin.delete("/{user_id}")
async def delete_user(user_id: int, current_user: User = Depends(get_active_user)):
    """Soft-delete a target user record by
    updating their status to inactive.

    Args:
        user_id (int): The database primary
        key identifier of the user to deactivate.
        current_user (User): The administrative
        user executing the action.

    Returns:
        dict: A confirmation dictionary indicating
        a successful soft-deletion step.
    """
    user = await UserService.get_user(user_id)
    return await UserService.deactivate_user(
        user=user,
        updated_by_id=current_user.id,
    )


@routerUser.put("/", response_model=UserResponse)
async def update_user(data: UserUpdate, current_user: User = Depends(get_active_user)):
    """Modify permitted registration data for
    the currently authenticated user.

    Args:
        data (UserUpdate): Validated Pydantic
        schema holding profile update attributes.
        current_user (User): The active authenticated
        User instance from dependency injection.

    Returns:
        UserResponse: The serialized entry of
        the freshly updated user record.
    """
    return await UserService.update_user(
        user=current_user,
        data=data,
    )


@routerUser.get("/profile", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_active_user)):
    """Fetch the active session profile details
    for the currently authenticated user.

    Args:
        current_user (User): The active authenticated
        User instance from dependency injection.

    Returns:
        UserResponse: The serialized details
        of the current authenticated user.
    """
    return current_user



@routerUser.delete("/")
async def deactivate_my_account(current_user: User = Depends(get_active_user)):
    """Self-trigger account deactivation (soft-delete)
    for the currently authenticated user.

    Args:
        current_user (User): The active authenticated
        User instance from dependency injection.

    Returns:
        dict: A confirmation dictionary signifying
        successful self-deactivation.
    """
    return await UserService.deactivate_user(
        user=current_user,
        updated_by_id=current_user.id,
    )

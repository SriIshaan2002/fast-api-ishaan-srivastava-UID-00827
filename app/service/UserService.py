"""
This module provides service operations for user management.
"""

from fastapi import HTTPException, status
from tortoise.exceptions import IntegrityError

from app.models import User
from app.schemas import UserCreate, UserUpdate
from constants import AUTH_ERRORS, SUCCESS_MESSAGES


class UserService:
    """Provides database operations for user management."""

    @staticmethod
    async def get_all_users() -> list[User]:
        """Retrieve all users."""
        return await User.all().order_by("id")

    @staticmethod
    async def get_user(user_id: int) -> User:
        """Retrieve a user by ID."""
        user = await User.get_or_none(id=user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=AUTH_ERRORS.user_not_found,
            )
        return user

    @staticmethod
    async def get_user_by_email(email: str) -> User:
        """Retrieve a user by email address."""
        user = await User.get_or_none(email=email.strip().lower())
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=AUTH_ERRORS.user_not_found
            )
        return user

    @staticmethod
    async def create_user(data: UserCreate) -> User:
        """Create a new user."""
        user_data = data.model_dump()
        user_data["email"] = str(user_data["email"]).strip().lower()
        try:
            return await User.create(**user_data)
        except IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=AUTH_ERRORS.user_already_exists,
            ) from exc

    @staticmethod
    async def update_user(user: User, data: UserUpdate) -> User:
        """Update permitted fields of a user's profile."""
        update_data = data.model_dump(exclude_unset=True)
        if "email" in update_data and update_data["email"] is not None:
            update_data["email"] = str(update_data["email"]).strip().lower()
        for field, value in update_data.items():
            setattr(user, field, value)

        if update_data:
            try:
                await user.save()
            except IntegrityError as exc:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=AUTH_ERRORS.user_already_exists,
                ) from exc
        return user

    @staticmethod
    async def deactivate_user(
        user: User,
        updated_by_id: int,
    ) -> dict[str, str]:
        """Soft-delete a user by marking the account inactive."""
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=AUTH_ERRORS.user_not_found,
            )

        user.is_active = False
        user.updated_by_id = updated_by_id
        await user.save()

        return {"message": SUCCESS_MESSAGES.user_deleted}

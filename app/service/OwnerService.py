"""
This module provides service operations for owners.
"""

from fastapi import HTTPException, status
from tortoise.exceptions import IntegrityError

from app.models import Owner
from app.schemas import OwnerCreate, OwnerUpdate
from constants import OWNER_ERRORS


class OwnerService:
    """Provides CRUD operations for owners."""

    @staticmethod
    async def create_owner(data: OwnerCreate) -> Owner:
        """Create a new owner."""
        try:
            return await Owner.create(
                username=data.username,
                email=str(data.email).lower(),
                mobile=data.mobile,
                password=data.password,
            )
        except IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=OWNER_ERRORS.already_exists,
            ) from exc

    @staticmethod
    async def get_all_owners() -> list[Owner]:
        """Retrieve all owners."""
        return await Owner.all().order_by("id")

    @staticmethod
    async def get_owner(owner_id: int) -> Owner:
        """Retrieve an owner by ID."""
        owner = await Owner.get_or_none(id=owner_id)
        if owner is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=OWNER_ERRORS.not_found,
            )
        return owner

    @staticmethod
    async def update_owner(
        owner_id: int,
        data: OwnerUpdate,
    ) -> Owner:
        """Update an owner's permitted fields."""
        owner = await OwnerService.get_owner(owner_id)
        changes = data.model_dump(exclude_unset=True)
        if "email" in changes and changes["email"] is not None:
            changes["email"] = str(changes["email"]).lower()
        for field, value in changes.items():
            setattr(owner, field, value)
        if changes:
            try:
                await owner.save()
            except IntegrityError as exc:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=OWNER_ERRORS.already_exists,
                ) from exc
        return owner

    @staticmethod
    async def delete_owner(owner_id: int) -> None:
        """Delete an owner."""
        owner = await OwnerService.get_owner(owner_id)
        await owner.delete()

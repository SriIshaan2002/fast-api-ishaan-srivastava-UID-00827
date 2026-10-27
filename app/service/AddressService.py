"""
This module provides service operations for user addresses.
"""

from fastapi import HTTPException, status

from app.models import Address
from app.schemas import AddressCreate, AddressUpdate
from constants import ADDRESS_ERRORS


class AddressService:
    """Provides CRUD operations for user addresses."""

    @staticmethod
    async def create_address(data: AddressCreate, user_id: int) -> Address:
        """Create an address for the authenticated user."""
        return await Address.create(
            user_id=user_id,
            **data.model_dump(),
        )

    @staticmethod
    async def get_all_addresses(user_id: int) -> list[Address]:
        """Retrieve active addresses belonging to the authenticated user."""
        return await Address.filter(
            user_id=user_id,
            is_active=True,
        ).order_by("id")

    @staticmethod
    async def get_address(address_id: int, user_id: int) -> Address:
        """Retrieve an address belonging to the authenticated user."""
        address = await Address.get_or_none(
            id=address_id,
            user_id=user_id,
            is_active=True,
        )

        if address is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ADDRESS_ERRORS.not_found,
            )

        return address

    @staticmethod
    async def update_address(
        address_id: int,
        data: AddressUpdate,
        user_id: int,
    ) -> Address:
        """Update an address belonging to the authenticated user."""
        address = await AddressService.get_address(
            address_id=address_id,
            user_id=user_id,
        )

        changes = data.model_dump(exclude_unset=True)

        for field, value in changes.items():
            setattr(address, field, value)

        if changes:
            await address.save()

        return address

    @staticmethod
    async def delete_address(address_id: int, user_id: int) -> None:
        """Delete an address belonging to the authenticated user."""
        address = await AddressService.get_address(
            address_id=address_id,
            user_id=user_id,
        )

        await address.delete()

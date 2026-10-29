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
        """Create and persist a new address record linked to a specific user.

        Args:
            data (AddressCreate):
            A validated Pydantic schema containing address creation details.
            user_id (int): The unique integer database ID of the owning user.

        Returns:
            Address: The newly created Address database instance.
        """
        return await Address.create(
            user_id=user_id,
            **data.model_dump(),
        )

    @staticmethod
    async def get_all_addresses(user_id: int) -> list[Address]:
        """Retrieve all active addresses belonging to a specific user, sorted by ID.

        Args:
            user_id (int): The unique integer database ID of the user.

        Returns:
            list[Address]:
              A list containing all matching active Address database instances.
        """
        return await Address.filter(
            user_id=user_id,
            is_active=True,
        ).order_by("id")

    @staticmethod
    async def get_address(address_id: int, user_id: int) -> Address:
        """Retrieve a specific active address
           matching the provided address and user IDs.

        Args:
            address_id (int): The unique integer database ID of the address.
            user_id (int): The unique integer database ID of the owning user.

        Returns:
            Address: The retrieved active Address database instance.

        Raises:
            HTTPException: 404 error if the address
            does not exist or is marked inactive.
        """
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
        """Update permitted attributes of an existing address belonging to the user.

        Args:
            address_id (int): The unique integer database ID of the address to update.
            data (AddressUpdate): A validated Pydantic schema holding fields to modify.
            user_id (int): The unique integer database ID of the owning user.

        Returns:
            Address: The updated and saved Address database instance.

        Raises:
            HTTPException: 404 error if the address is not found or inaccessible.
        """
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
        """Permanently delete an address record from the database.

        Args:
            address_id (int): The unique integer database ID of the address to delete.
            user_id (int): The unique integer database ID of the owning user.

        Raises:
            HTTPException: 404 error if the address is not found or inaccessible.
        """
        address = await AddressService.get_address(
            address_id=address_id,
            user_id=user_id,
        )

        await address.delete()

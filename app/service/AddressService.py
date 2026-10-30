"""
This module provides service operations for user addresses.
"""

from app.exception import AddressNotFoundError
from app.models import Address
from app.schemas import AddressCreate


class AddressService:
    """Provides CRUD operations for user addresses."""

    @staticmethod
    async def create_address(data: AddressCreate, user_id: int) -> Address:
        """Create a new address linked to a specific user.

        Args:
            data (AddressCreate): Validated address creation details.
            user_id (int): ID of the owning user.

        Returns:
            Address: Newly created address instance.
        """
        return await Address.create(
            user_id=user_id,
            **data.model_dump(),
        )

    @staticmethod
    async def get_all_addresses(user_id: int) -> list[Address]:
        """Retrieve all active addresses belonging to a user.

        Args:
            user_id (int): ID of the owning user.

        Returns:
            list[Address]: List of active addresses.
        """
        return await Address.filter(
            user_id=user_id,
            is_active=True,
        ).order_by("id")

    @staticmethod
    async def get_address(address_id: int, user_id: int) -> Address:
        """Retrieve an active address belonging to a user.

        Args:
            address_id (int): ID of the address.
            user_id (int): ID of the owning user.

        Returns:
            Address: Retrieved address instance.

        Raises:
            AddressNotFoundError: If the address does not exist,
                is inactive, or does not belong to the user.
        """
        address = await Address.get_or_none(
            id=address_id,
            user_id=user_id,
            is_active=True,
        )

        if address is None:
            raise AddressNotFoundError()

        return address

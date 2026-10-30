"""
This module provides service operations for user addresses.
"""

from app.exception import AddressNotFoundError, RegisteredEmail
from app.models import Address
from app.schemas import AddressCreate, AddressUpdate, AddressResponse
from tortoise.exceptions import IntegrityError
from fastapi import HTTPException, status
from constants import ADDRESS_ERRORS

class AddressService:
    """Provides CRUD operations for user addresses."""

    @staticmethod
    async def create_address(data: AddressCreate, user_id: int) -> AddressResponse:
        """Create a new address linked to a specific user.

        Args:
            data (AddressCreate): Validated address creation details.
            user_id (int): ID of the owning user.

        Returns:
            Address: Newly created address instance.
        """
        address = await Address.create(
            user_id=user_id,
            **data.model_dump(),
        )

        return AddressResponse.model_validate(address)

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

    @staticmethod
    async def update_address(address_id: int, user_id: int, address: AddressUpdate) -> AddressResponse:
        """Update an address by soft-deleting the active record and generating a new instance.

        Arguments:
            address_id: The ID of the existing address to replace.
            user_id: The unique identifier of the owner.
            address: The schema data containing updated address fields.

        Returns:
            The validated response schema containing the new address details.

        Raises:
            AddressNotFoundError: If the target address does not exist or belongs to another user.
            Registered Email: for conflict
        """
        current_address = await Address.get_or_none(
            id=address_id,
            user_id=user_id,
            is_active=True,
        )

        if current_address is None:
            raise AddressNotFoundError()

        current_address.is_active = False
        await current_address.save(update_fields=["is_active"])

        try:
            new_address_data = {
                "city": current_address.city,
                "street": current_address.street,
                "house": current_address.house,
                "zip": current_address.zip,
                "nearby_location": current_address.nearby_location,
                "long": current_address.long,
                "lat": current_address.lat,
            }
            incoming_updates = address.model_dump(exclude_unset=True)
            new_address_data.update(incoming_updates)
            
            new_address_data["user_id"] = user_id
            new_address_data["is_active"] = True
            
            new_address = await Address.create(**new_address_data)
            
        except IntegrityError as exc:
            current_address.is_active = True
            await current_address.save(update_fields=["is_active"])
            
            raise RegisteredEmail()

        return AddressResponse.model_validate(new_address)

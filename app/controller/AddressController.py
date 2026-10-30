"""
This module provides CRUD routes for user addresses.
"""

from typing import Annotated

from fastapi import Depends, status

from app.dependency.dependency import get_active_user
from app.models import User
from app.schemas import AddressCreate, AddressResponse
from app.service.AddressService import AddressService
from app.routes import routerAdress

CurrentUser = Annotated[User, Depends(get_active_user)]


@routerAdress.post(
    "/",
    response_model=AddressResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_address(
    data: AddressCreate,
    current_user: CurrentUser,
):
    """Create a new address record linked to the authenticated session user.

    Args:
        data (AddressCreate): Validated Pydantic schema containing creation details.
        current_user (CurrentUser):
        The active authenticated User instance from dependency injection.

    Returns:
        AddressResponse: The serialized data of the newly created address.
    """
    return await AddressService.create_address(
        data=data,
        user_id=current_user.id,
    )


@routerAdress.get("/", response_model=list[AddressResponse])
async def get_all_addresses(current_user: CurrentUser):
    """Retrieve a list of all active addresses
    belonging to the authenticated session user.

    Args:
        current_user (CurrentUser): The active
        authenticated User instance from dependency injection.

    Returns:
        list[AddressResponse]: A list containing
        serialized representations of active addresses.
    """
    return await AddressService.get_all_addresses(
        user_id=current_user.id,
    )


@routerAdress.get("/{address_id}", response_model=AddressResponse)
async def get_address(
    address_id: int,
    current_user: CurrentUser,
):
    """Retrieve a single active address belonging
      to the authenticated session user by ID.

    Args:
        address_id (int): The database primary
        key identifier of the targeted address.
        current_user (CurrentUser): The active
        authenticated User instance from dependency injection.

    Returns:
        AddressResponse: The serialized entry of the requested address.
    """
    return await AddressService.get_address(
        address_id=address_id,
        user_id=current_user.id,
    )

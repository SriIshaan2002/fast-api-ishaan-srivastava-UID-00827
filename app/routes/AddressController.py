"""
This module provides CRUD routes for user addresses.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.dependency.dependency import get_active_user
from app.models import User
from app.schemas import AddressCreate, AddressResponse, AddressUpdate
from app.service.AddressService import AddressService

router = APIRouter(
    prefix="/addresses", tags=["Addresses"], dependencies=[Depends(get_active_user)]
)

CurrentUser = Annotated[User, Depends(get_active_user)]


@router.post(
    "/",
    response_model=AddressResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_address(
    data: AddressCreate,
    current_user: CurrentUser,
):
    """Create an address for the authenticated user."""
    return await AddressService.create_address(
        data=data,
        user_id=current_user.id,
    )


@router.get("/", response_model=list[AddressResponse])
async def get_all_addresses(current_user: CurrentUser):
    """Retrieve addresses belonging to the authenticated user."""
    return await AddressService.get_all_addresses(
        user_id=current_user.id,
    )


@router.get("/{address_id}", response_model=AddressResponse)
async def get_address(
    address_id: int,
    current_user: CurrentUser,
):
    """Retrieve one address belonging to the authenticated user."""
    return await AddressService.get_address(
        address_id=address_id,
        user_id=current_user.id,
    )


@router.patch("/{address_id}", response_model=AddressResponse)
async def update_address(
    address_id: int,
    data: AddressUpdate,
    current_user: CurrentUser,
):
    """Update an address belonging to the authenticated user."""
    return await AddressService.update_address(
        address_id=address_id, data=data, user_id=current_user.id
    )


@router.delete(
    "/{address_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_address(
    address_id: int,
    current_user: CurrentUser,
) -> None:
    """Delete an address belonging to the authenticated user."""
    await AddressService.delete_address(
        address_id=address_id,
        user_id=current_user.id,
    )

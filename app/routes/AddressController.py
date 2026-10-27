"""
This module provides CRUD operations for user addresses.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependency.dependency import get_active_user
from app.models import Address
from app.schemas import AddressCreate, AddressResponse, AddressUpdate
from constants import ADDRESS_ERRORS

router = APIRouter(
    prefix="/addresses", tags=["Addresses"], dependencies=[Depends(get_active_user)]
)


@router.post(
    "/",
    response_model=AddressResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_address(data: AddressCreate, current_user=Depends(get_active_user)):
    """Create an address for the authenticated user."""
    address = await Address.create(
        user_id=current_user.id,
        **data.model_dump(),
    )
    return address


@router.get("/", response_model=list[AddressResponse])
async def get_all_addresses(current_user=Depends(get_active_user)):
    """Retrieve addresses belonging to the authenticated user."""
    return await Address.filter(user_id=current_user.id, is_active=True).order_by("id")


@router.get("/{address_id}", response_model=AddressResponse)
async def get_address(
    address_id: int,
    current_user=Depends(get_active_user),
):
    """Retrieve one address belonging to the authenticated user."""
    address = await Address.get_or_none(
        id=address_id,
        user_id=current_user.id,
    )
    if address is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ADDRESS_ERRORS.not_found,
        )
    return address


@router.patch("/{address_id}", response_model=AddressResponse)
async def update_address(
    address_id: int, data: AddressUpdate, current_user=Depends(get_active_user)
):
    """Update an address belonging to the authenticated user."""
    address = await Address.get_or_none(
        id=address_id,
        user_id=current_user.id,
    )

    if address is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ADDRESS_ERRORS.not_found,
        )
    changes = data.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(address, field, value)
    if changes:
        await address.save()
    return address


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(
    address_id: int,
    current_user=Depends(get_active_user),
):
    """Delete an address belonging to the authenticated user."""
    address = await Address.get_or_none(
        id=address_id,
        user_id=current_user.id,
    )
    if address is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ADDRESS_ERRORS.not_found,
        )
    await address.delete()

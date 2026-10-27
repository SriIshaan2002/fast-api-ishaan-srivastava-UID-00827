"""
This module provides CRUD routes for owners.
"""

from fastapi import APIRouter, Depends, status

from app.dependency.dependency import get_active_user
from app.schemas import OwnerCreate, OwnerResponse, OwnerUpdate
from app.service.OwnerService import OwnerService

router = APIRouter(
    prefix="/owners", tags=["Owners"], dependencies=[Depends(get_active_user)]
)


@router.post("/", response_model=OwnerResponse, status_code=status.HTTP_201_CREATED)
async def create_owner(data: OwnerCreate):
    """Create a new owner."""
    return await OwnerService.create_owner(data)




@router.get("/", response_model=list[OwnerResponse])
async def get_all_owners():
    """Retrieve all owners."""
    return await OwnerService.get_all_owners()




@router.get("/{owner_id}", response_model=OwnerResponse)
async def get_owner(owner_id: int):
    """Retrieve an owner by ID."""
    return await OwnerService.get_owner(owner_id)




@router.patch("/{owner_id}", response_model=OwnerResponse)
async def update_owner(owner_id: int, data: OwnerUpdate):
    """Update an owner's permitted fields."""
    return await OwnerService.update_owner(owner_id=owner_id, data=data)


@router.delete("/{owner_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_owner(owner_id: int) -> None:
    """Delete an owner."""
    await OwnerService.delete_owner(owner_id)

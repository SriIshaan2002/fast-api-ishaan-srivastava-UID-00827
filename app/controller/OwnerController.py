"""
This module provides CRUD routes for owners.
"""

from fastapi import APIRouter, Depends, status

from app.dependency.dependency import get_active_user
from app.schemas import OwnerCreate, OwnerResponse
from app.service.OwnerService import OwnerService
from app.routes import routerAdmin
from app.routes import routerOwner


@routerAdmin.post("/", response_model=OwnerResponse, status_code=status.HTTP_201_CREATED)
async def create_owner(data: OwnerCreate):
    """Create a new mapping record associating a user with a restaurant they own.

    Args:
        data (OwnerCreate): Validated Pydantic
        schema containing user_id and restraunt_id.

    Returns:
        OwnerResponse: The serialized entry
        of the newly created ownership record.
    """
    return await OwnerService.create_owner(data)


@routerAdmin.get("/", response_model=list[OwnerResponse])
async def get_all_owners():
    """Retrieve all user-restaurant ownership assignment records.

    Returns:
        list[OwnerResponse]: A list containing
        serialized representations of all ownership entries.
    """
    return await OwnerService.get_all_owners()


@routerOwner.get("/{owner_id}", response_model=OwnerResponse)
async def get_owner(owner_id: int):
    """Retrieve a specific ownership
    association entry by its unique database ID.

    Args:
        owner_id (int): The database primary
        key identifier of the ownership mapping.

    Returns:
        OwnerResponse: The serialized entry
        of the requested ownership record.
    """
    return await OwnerService.get_owner(owner_id)



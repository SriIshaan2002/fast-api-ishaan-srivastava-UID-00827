"""
This module provides CRUD routes for owners.
"""

from fastapi import status

from app.routes.OwnerRoutes import routerOwner
from app.schemas import OwnerCreate, OwnerResponse
from app.service.OwnerService import OwnerService


@routerOwner.post(
    "/", response_model=OwnerResponse, status_code=status.HTTP_201_CREATED
)
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
    return await OwnerService.get_owner(owner_id=owner_id)

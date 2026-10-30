"""
This module provides CRUD API endpoints for managing restaurant operations.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.dependency.dependency import get_active_user
from app.models import User
from app.schemas import RestrauntCreate, RestrauntResponse, RestrauntUpdate
from app.service.RestrauntService import (
    create_restaurant as create_restaurant_service,
    delete_restaurant as delete_restaurant_service,
    get_restaurant as get_restaurant_service,
    get_restaurants as get_restaurants_service,
    update_restaurant as update_restaurant_service,
)
from app.routes.RestrauntRoutes import restaurant_router

CurrentUser = Annotated[User, Depends(get_active_user)]


@restaurant_router.post(
    "/", response_model=RestrauntResponse, status_code=status.HTTP_201_CREATED
)
async def create_restaurant(
    payload: RestrauntCreate,
    current_user: CurrentUser,
):
    """Create a new restaurant and link the authenticated session user as an owner.

    Args:
        payload (RestrauntCreate): Validated Pydantic schema containing initial restaurant fields.
        current_user (CurrentUser): The active authenticated User instance from dependency injection.

    Returns:
        RestrauntResponse: The serialized model instance data of the created restaurant.
    """
    return await create_restaurant_service(payload=payload, current_user=current_user)


@restaurant_router.get("/", response_model=list[RestrauntResponse])
async def get_restaurants():
    """Retrieve all active restaurants in the database.

    Returns:
        list[RestrauntResponse]: A list containing serialized instances of active restaurants.
    """
    return await get_restaurants_service()


@restaurant_router.get("/{restaurant_id}", response_model=RestrauntResponse)
async def get_restaurant(restaurant_id: int):
    """Retrieve a single active restaurant by its primary key ID.

    Args:
        restaurant_id (int): The unique integer database ID of the restaurant.

    Returns:
        RestrauntResponse: The serialized entry of the requested restaurant record.
    """
    return await get_restaurant_service(restaurant_id=restaurant_id)


@restaurant_router.put(
    "/{restaurant_id}",
    response_model=RestrauntResponse,
)
async def update_restaurant(
    restaurant_id: int, payload: RestrauntUpdate, current_user: CurrentUser
):
    """Modify the parameters of an existing active restaurant record.

    Args:
        restaurant_id (int): The unique integer database ID of the restaurant to update.
        payload (RestrauntUpdate): Validated Pydantic schema containing modification properties.
        current_user (CurrentUser): The active authenticated User instance from dependency injection.

    Returns:
        RestrauntResponse: The serialized entry of the updated restaurant data.
    """
    return await update_restaurant_service(
        restaurant_id=restaurant_id, payload=payload, current_user=current_user
    )


@restaurant_router.delete(
    "/{restaurant_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_restaurant(
    restaurant_id: int,
    current_user: CurrentUser,
):
    """Flag an active restaurant record as inactive (soft-delete).

    Args:
        restaurant_id (int): The unique integer database ID of the restaurant to remove.
        current_user (CurrentUser): The active authenticated User instance from dependency injection.
    """
    await delete_restaurant_service(
        restaurant_id=restaurant_id, current_user=current_user
    )

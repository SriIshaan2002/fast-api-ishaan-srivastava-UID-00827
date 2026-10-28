from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.dependency.dependency import get_active_user
from app.models import User
from app.schemas import RestrauntCreate, RestrauntResponse, RestrauntResponse
from app.service.RestrauntService import (
    create_restaurant as create_restaurant_service,
    delete_restaurant as delete_restaurant_service,
    get_restaurant as get_restaurant_service,
    get_restaurants as get_restaurants_service,
    update_restaurant as update_restaurant_service,
)

CurrentUser = Annotated[User, Depends(get_active_user)]

restaurant_router = APIRouter(
    prefix="/restaurants", tags=["Restaurants"], dependencies=[Depends(get_active_user)]
)


@restaurant_router.post(
    "/", response_model=RestrauntResponse, status_code=status.HTTP_201_CREATED
)
async def create_restaurant(
    payload: RestrauntCreate,
    current_user: CurrentUser,
):
    """Create a restaurant and associate its creator as an owner."""
    return await create_restaurant_service(payload=payload, current_user=current_user)


@restaurant_router.get("/", response_model=list[RestrauntResponse])
async def get_restaurants():
    """Return all active restaurants."""
    return await get_restaurants_service()


@restaurant_router.get("/{restaurant_id}", response_model=RestrauntResponse)
async def get_restaurant(restaurant_id: int):
    """Return an active restaurant by ID."""
    return await get_restaurant_service(restaurant_id=restaurant_id)


@restaurant_router.put(
    "/{restaurant_id}",
    response_model=RestrauntResponse,
)
async def update_restaurant(
    restaurant_id: int, payload: RestrauntResponse, current_user: CurrentUser
):
    """Update an active restaurant."""
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
    """Soft-delete an active restaurant."""
    await delete_restaurant_service(
        restaurant_id=restaurant_id, current_user=current_user
    )

"""This module provides FastAPI routing endpoints for managing restaurant menu items."""

from fastapi import APIRouter, Depends, status
from app.schemas.items import ItemCreate, ItemUpdate, ItemResponse
from app.service.ItemService import ItemService
from app.models import User
from app.dependency.dependency import get_active_user  
from app.routes.ItemRoutes import routerItems

@routerItems.post(
    "/", 
    response_model=ItemResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new menu item"
)
async def create_item(
    payload: ItemCreate,
    current_user: User = Depends(get_active_user)
) -> ItemResponse:
    """Create a new menu item bound to a restaurant after verifying owner authorization."""
    return await ItemService.create_item(data=payload, current_user=current_user)


@routerItems.get(
    "/restaurant/{restaurant_id}", 
    response_model=list[ItemResponse],
    summary="Get restaurant menu"
)
async def get_restaurant_menu(restaurant_id: int) -> list[ItemResponse]:
    """Fetch all active available menu items registered to a given restaurant ID."""
    return await ItemService.get_restaurant_menu(restaurant_id=restaurant_id)


@routerItems.get(
    "/{item_id}", 
    response_model=ItemResponse,
    summary="Get single menu item"
)
async def get_item(item_id: int) -> ItemResponse:
    """Retrieve a specific active item configuration by its primary key index."""
    return await ItemService.get_item(item_id=item_id)


@routerItems.post(
    "/{item_id}", 
    response_model=ItemResponse,
    summary="Update a menu item"
)
async def update_item(
    item_id: int,
    payload: ItemUpdate,
    current_user: User = Depends(get_active_user)
) -> ItemResponse:
    """Modify fields of an existing menu item record after checking access permissions."""
    return await ItemService.update_item(
        item_id=item_id, 
        data=payload, 
        current_user=current_user
    )


@routerItems.delete(
    "/{item_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Soft-delete a menu item"
)
async def delete_item(
    item_id: int,
    current_user: User = Depends(get_active_user)
) -> None:
    """Flag a specific menu item as inactive (soft-delete) after checking ownership access."""
    await ItemService.delete_item(item_id=item_id, current_user=current_user)

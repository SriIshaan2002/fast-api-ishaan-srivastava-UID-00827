"""
This module provides operational API endpoints
for managing the customer order lifecycle.
"""

from typing import Annotated

from fastapi import Depends, status

from app.dependency.dependency import get_active_user
from app.exception.CustomException import OrderNotFoundError
from app.models import User
from app.routes.OrderRouter import orderRouter
from app.schemas.items import MenuItemOut
from app.schemas.orders import OrderCreate, OrderOut, OrderResponse
from app.schemas.restraunt import RestaurantOut
from app.service import RestrauntService
from app.service.OrderService import OrderService

CurrentUser = Annotated[User, Depends(get_active_user)]


@orderRouter.post(
    "/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED
)
async def create_order(
    payload: OrderCreate,
    current_user: CurrentUser,
):
    """Instantiate a brand-new restaurant order entry
    and track individual purchase line items.

    Args:
        payload (OrderCreate): Validated Pydantic schema
        detailing the restaurant targets and item counts.
        current_user (CurrentUser): The active authenticated
        User instance extracted from the security token.

    Returns:
        OrderResponse: The Pydantic-serialized JSON summary
        details of the successfully processed order.
    """
    return await OrderService.create_order(data=payload, current_user=current_user)


@orderRouter.get("/orders/{order_id}", response_model=OrderOut)
async def get_order(order_id: int, current_user: CurrentUser):
    """
    Retrieve details of a specific order.

    Fetches the details of an order using its unique ID, provided it belongs
    to the currently authenticated user. If the order does not exist or
    does not belong to the user, a 404 error is returned to prevent info leakage.

    Args:
        order_id (int): The unique identifier of the order.
        current_user (CurrentUser): The authenticated user making the request.

    Returns:
        OrderOut: The complete details of the requested order.

    Raises:
        HTTPException: 404 status code if the order is not found or inaccessible.
    """
    try:
        return await OrderService.get_order(order_id, current_user.id)
    except OrderNotFoundError as e:
        raise e


@orderRouter.get("/", response_model=list[RestaurantOut])
async def list_restaurants(current_user: CurrentUser):
    """
    List active restaurants sorted by most recent order.

    Retrieves a list of all currently active restaurants. The results are
    ordered dynamically based on the timestamp of their most recent order,
    placing the most recently active restaurants first.

    Args:
        current_user (CurrentUser): The authenticated user making the request.

    Returns:
        list[RestaurantOut]: A list of active restaurants with their details.
    """
    return await RestrauntService.list_by_recent_order()


@orderRouter.get("/{restaurant_id}/items", response_model=list[MenuItemOut])
async def get_menu(restaurant_id: int):
    """
    Fetch all available menu items of a specific restaurant.

    Public endpoint that allows any user (authenticated or anonymous) to view
    the full menu of a given restaurant by its ID. Only returns items that
    are currently marked as available.

    Args:
        restaurant_id (int): The unique identifier of the restaurant.

    Returns:
        list[MenuItemOut]: A list of available menu items for the restaurant.
    """
    return await RestrauntService.get_menu(restaurant_id)

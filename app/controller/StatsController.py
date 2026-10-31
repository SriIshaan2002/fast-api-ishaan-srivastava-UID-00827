from fastapi import APIRouter, Depends, Query, HTTPException

from app.dependency.dependency import get_active_user
from app.models.model import User
from app.schemas.stats import MenuItemStat, OrderPage, TopCustomer
from app.service.StatsService import RestaurantStatsService
from enums import OrderStatus

router = APIRouter(prefix="/owners/restaurants", tags=["Owner"])


@router.get("/{restaurant_id}/stats/items", response_model=list[MenuItemStat])
async def menu_item_stats(
    restaurant_id: int, current_user: User = Depends(get_active_user)
):
    """Retrieve performance statistics for all menu items in a specific restaurant.

    Args:
        restaurant_id (int): The unique integer database ID of the restaurant.
        current_user (User): The authenticated active user session injected by the dependency.

    Returns:
        list[MenuItemStat]: A list of structured Pydantic response items containing order counts, 
            popularity tracking, and gross revenue generated per menu item.

    Raises:
        HTTPException: 401 Unauthorized if the user session context is unverified.
        HTTPException: 403 Forbidden if the current user is not the authorized owner of the restaurant.
        HTTPException: 404 Not Found if the targeted restaurant configuration does not exist.
    """
    return await RestaurantStatsService.menu_item_stats(restaurant_id, current_user)


@router.get("/{restaurant_id}/stats/top-customers", response_model=list[TopCustomer])
async def top_customers(
    restaurant_id: int,
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_active_user),
):
    """Fetch the top highest-spending customers for a given restaurant storefront.

    Args:
        restaurant_id (int): The unique integer database ID of the restaurant.
        limit (int, optional): The maximum number of customer metrics records to fetch. 
            Must be between 1 and 100 inclusive. Defaults to 10.
        current_user (User): The authenticated active user session injected by the dependency.

    Returns:
        list[TopCustomer]: A list of objects detailing customer profiles alongside their total 
            monetary expenditure and aggregate order metrics count.

    Raises:
        HTTPException: 401 Unauthorized if the session credentials fail verification.
        HTTPException: 403 Forbidden if the user lacks access rights for this restaurant's metrics.
        HTTPException: 422 Unprocessable Entity if the limit constraint parameter violates bounds.
    """
    return await RestaurantStatsService.top_customers(
        restaurant_id, current_user, limit
    )


@router.get("/{restaurant_id}/orders", response_model=OrderPage)
async def list_restaurant_orders(
    restaurant_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: OrderStatus | None = None,
    current_user: User = Depends(get_active_user),
):
    """Retrieve a paginated list of orders placed at a specific restaurant storefront.

    Allows structural filtering options based on order status indicators to manage operational workflows.

    Args:
        restaurant_id (int): The unique integer database ID of the restaurant.
        page (int, optional): The target page index number for dataset separation. Must be >= 1. Defaults to 1.
        page_size (int, optional): The maximum volume of entries to populate per page array. 
            Must be between 1 and 100 inclusive. Defaults to 20.
        status (OrderStatus | None, optional): An optional filter parameter matching specific lifecycle 
            states (e.g., PENDING, COMPLETED). Defaults to None.
        current_user (User): The authenticated active user session injected by the dependency.

    Returns:
        OrderPage: A paginated envelope schema encapsulating the list of order structures alongside 
            dataset pagination metadata (total counts, current page tracking indexes).

    Raises:
        HTTPException: 401 Unauthorized if the calling session lacks valid credential states.
        HTTPException: 403 Forbidden if the user is not the confirmed manager/owner of the restaurant.
        HTTPException: 422 Unprocessable Entity if paging constraints or query values fail syntax requirements.
    """
    return await RestaurantStatsService.list_orders(
        restaurant_id, current_user, page, page_size, status
    )

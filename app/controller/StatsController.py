from fastapi import APIRouter, Depends, Query

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
    return await RestaurantStatsService.menu_item_stats(restaurant_id, current_user)


@router.get("/{restaurant_id}/stats/top-customers", response_model=list[TopCustomer])
async def top_customers(
    restaurant_id: int,
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_active_user),
):
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
    return await RestaurantStatsService.list_orders(
        restaurant_id, current_user, page, page_size, status
    )

from tortoise.functions import Count, Sum
from app.models.model import Restraunt, User, OrderItem, OrderStatus, Order
from app.exception.AuthException import RestrauntNotFound
from app.schemas.stats import MenuItemStat, TopCustomer, OrderPage, OrderListItem


class RestaurantStatsService:
    @staticmethod
    async def _get_owned_restaurant(restaurant_id: int, owner: User) -> Restraunt:
        """Return the restaurant only if `owner` created it.

        Raises:
            RestrauntNotFound: If missing or owned by someone else
                (same error for both, so IDs can't be probed).
        """
        restaurant = await Restraunt.get_or_none(
            id=restaurant_id, created_by_id=owner.id, is_active=True
        )
        if restaurant is None:
            raise RestrauntNotFound()
        return restaurant

    @staticmethod
    async def menu_item_stats(restaurant_id: int, owner: User) -> list[MenuItemStat]:
        """Per menu item: how many times ordered and total units sold."""
        await RestaurantStatsService._get_owned_restaurant(restaurant_id, owner)

        rows = (
            await OrderItem.filter(order__restaurant_id=restaurant_id)
            .exclude(order__status=OrderStatus.CANCELLED)
            .annotate(times_ordered=Count("id"), total_quantity=Sum("quantity"))
            .group_by("item_name")
            .order_by("-total_quantity")
            .values("item_name", "times_ordered", "total_quantity")
        )
        return [MenuItemStat(**row) for row in rows]

    @staticmethod
    async def top_customers(
        restaurant_id: int, owner: User, limit: int = 10
    ) -> list[TopCustomer]:
        """Customers ranked by number of orders at this restaurant."""
        await RestaurantStatsService._get_owned_restaurant(restaurant_id, owner)

        rows = await (
                        Order.filter(restaurant_id=restaurant_id)
                        .group_by("user_id", "user__username")
                        .annotate(order_count=Count("id"), total_spent=Sum("total_price"))
                        .order_by("-total_spent")
                        .limit(limit)
                        .values("user_id", "user__username", "order_count", "total_spent")
                    )

        return [
            TopCustomer(
                user_id=r["user_id"],
                name=r["user__username"],
                order_count=r["order_count"],
                total_spent=r["total_spent"],
            )
            for r in rows
        ]

    @staticmethod
    async def list_orders(
        restaurant_id: int,
        owner: User,
        page: int = 1,
        page_size: int = 20,
        status: OrderStatus | None = None,
    ) -> OrderPage:
        """Paginated list of all orders for the restaurant, newest first."""
        await RestaurantStatsService._get_owned_restaurant(restaurant_id, owner)

        query = Order.filter(restaurant_id=restaurant_id)
        if status:
            query = query.filter(status=status)

        total = await query.count()
        orders = (
            await query.order_by("-created_at")
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        return OrderPage(
            total=total,
            page=page,
            page_size=page_size,
            results=[OrderListItem.model_validate(o) for o in orders],
        )

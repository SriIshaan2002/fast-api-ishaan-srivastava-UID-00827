"""This module provides aggregation and paginated
reporting services for restaurant statistics."""

from tortoise.functions import Count, Sum

from app.exception.AuthException import RestrauntNotFound
from app.models.model import Order, OrderItem, OrderStatus, Restraunt, User
from app.schemas.stats import MenuItemStat, OrderListItem, OrderPage, TopCustomer


class RestaurantStatsService:
    """Provides reporting functionality for tracking restaurant operation summaries."""

    @staticmethod
    async def _get_owned_restaurant(restaurant_id: int, owner: User) -> Restraunt:
        """Return the restaurant only if the matching owner created it.

        Arguments:
            restaurant_id: The primary key index of the target restaurant record.
            owner: The authenticated user profile verifying ownership constraints.

        Returns:
            The matching verified active Restraunt model instance.

        Raises:
            RestrauntNotFound: If the restaurant is missing,
              inactive, or owned by someone else.
        """
        restaurant = await Restraunt.get_or_none(
            id=restaurant_id, created_by_id=owner.id, is_active=True
        )
        if restaurant is None:
            raise RestrauntNotFound()
        return restaurant

    @staticmethod
    async def menu_item_stats(restaurant_id: int, owner: User) -> list[MenuItemStat]:
        """Calculate the frequency of orders and
        the total volumetric quantity sold per menu item.

        Arguments:
            restaurant_id: The primary key index of the target restaurant record.
            owner: The authenticated operator initiating the analytical collection step.

        Returns:
            A list of validated summary metrics mapped across active menu items.

        Raises:
            RestrauntNotFound: If authorization checks
            drop or the record target is missing.
        """
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
        """Rank purchasing consumers according to total spent cumulative orders.

        Arguments:
            restaurant_id: The primary key index of the target restaurant record.
            owner: The authenticated operator
            initiating the analytical collection step.
            limit: The maximum size constraint threshold of customer records to fetch.

        Returns:
            A list of tracked customer profile
            records ordered from highest to lowest spent.

        Raises:
            RestrauntNotFound: If authorization
            checks drop or the record target is missing.
        """
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
        """Provide a paginated tracking summary containing recent order entries.

        Arguments:
            restaurant_id: The primary key index of the target restaurant record.
            owner: The authenticated operator initiating the analytical collection step.
            page: The targeted active index sequence frame location parameter.
            page_size: The targeted maximum
            slice pagination container density threshold.
            status: An optional filtering parameter to isolate specific tracking states.

        Returns:
            A structured reporting object containing
            total size metrics and matching results.

        Raises:
            RestrauntNotFound: If authorization checks
            drop or the record target is missing.
        """
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

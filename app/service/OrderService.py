"""
This module provides service operations for managing customer orders and transactions.
"""

from decimal import Decimal
from uuid import UUID

from tortoise.exceptions import IntegrityError, OperationalError
from tortoise.transactions import in_transaction

from app.exception.AuthException import (
    AddressNotFoundError,
    InsufficientStockError,
    InvalidQuantityError,
    ItemNotFoundError,
    OrderConflictError,
    OrderEmptyError,
    OrderNotFoundError,
    RestrauntNotFound,
)
from app.models import Address, Item, Order, OrderItem, Restraunt, User
from app.schemas.orders import (
    OrderAddressOut,
    OrderCreate,
    OrderItemOut,
    OrderOut,
    OrderRestaurantOut,
)
from enums import OrderStatus


class OrderService:
    """Provides atomic business logic operations for processing order details."""

    @staticmethod
    async def create_order(data: OrderCreate, current_user: User) -> Order:
        """Process and persist a new customer order with stock checks.

        Menu items are locked in ascending item ID
        order to avoid deadlocks. Duplicate item IDs in the request are merged
        before locking. Everything runs in one transaction, so any failure rolls
        back the stock decrements.

        Args:
            data (OrderCreate): Validated schema containing restaurant, delivery
                location, and item list.
            current_user (User): The authenticated user placing the order.

        Returns:
            Order: The newly created order.

        Raises:
            OrderEmptyError: If the item list is empty.
            InvalidQuantityError: If any requested quantity is 0 or negative.
            RestrauntNotFound: If the restaurant is missing or inactive.
            AddressNotFoundError: If the address is missing, inactive, or does
                not belong to the user.
            ItemNotFoundError: If an item does not exist or does not belong to
                the restaurant.
            InsufficientStockError: If a requested quantity exceeds stock.
            OrderConflictError: On an integrity error or lock/deadlock failure.
        """
        if not data.items:
            raise OrderEmptyError()
        requested: dict = {}
        for line in data.items:
            if line.quantity <= 0:
                raise InvalidQuantityError(line.item_id)
            requested[line.item_id] = requested.get(line.item_id, 0) + line.quantity

        restaurant_exists = await Restraunt.filter(
            id=data.restaurant_id, is_active=True
        ).exists()
        if not restaurant_exists:
            raise RestrauntNotFound()

        address_exists = await Address.filter(
            id=data.delivery_location_id,
            user_id=current_user.id,
            is_active=True,
        ).exists()
        if not address_exists:
            raise AddressNotFoundError()

        try:
            async with in_transaction():
                total_order_price = Decimal("0.000")
                validated_items_list = []

                for item_id in sorted(requested):
                    quantity = requested[item_id]

                    menu_item = (
                        await Item.filter(
                            id=item_id,
                            restaurant_id=data.restaurant_id,
                            is_active=True,
                        )
                        .select_for_update()
                        .first()
                    )

                    if not menu_item:
                        raise ItemNotFoundError(item_id)

                    if menu_item.quantity < quantity:
                        raise InsufficientStockError(
                            menu_item.item_name, menu_item.quantity, quantity
                        )

                    menu_item.quantity -= quantity
                    await menu_item.save(update_fields=["quantity"])

                    total_order_price += Decimal(menu_item.price) * quantity
                    validated_items_list.append((menu_item, quantity))

                order = await Order.create(
                    user=current_user,
                    restaurant_id=data.restaurant_id,
                    delivery_location_id=data.delivery_location_id,
                    total_price=total_order_price.quantize(Decimal("0.001")),
                    status=OrderStatus.PENDING,
                )

                await OrderItem.bulk_create(
                    [
                        OrderItem(
                            order=order,
                            item_name=menu_item.item_name,
                            is_veg=menu_item.is_veg,
                            quantity=quantity,
                            price=menu_item.price,
                        )
                        for menu_item, quantity in validated_items_list
                    ]
                )

            return order
        except (IntegrityError, OperationalError) as exc:
            raise OrderConflictError() from exc

    @staticmethod
    async def get_order(order_id: int, user_id: UUID) -> OrderOut:
        """Fetch a single order owned by the given user.

        Loads the order together with its restaurant, delivery address and
        active items. The lookup is scoped by user_id so a customer can
        never read another customer's order.

        Args:
            order_id: Identifier of the order to fetch.
            user_id: Identifier of the user making the request.

        Returns:
            The order with its restaurant, delivery location and active
            items, each item including its computed line total.

        Raises:
            OrderNotFoundError: If no order with order_id exists for user_id.
        """
        order = (
            await Order.filter(id=order_id, user_id=user_id)
            .select_related("restaurant", "delivery_location")
            .prefetch_related("order_items")
            .first()
        )

        if order is None:
            raise OrderNotFoundError(order_id)

        items = [
            OrderItemOut(
                id=item.id,
                item_name=item.item_name,
                is_veg=item.is_veg,
                quantity=item.quantity,
                discount=item.discount,
                price=item.price,
                line_total=OrderService._line_total(item),
            )
            for item in order.order_items
            if item.is_active
        ]

        return OrderOut(
            id=order.id,
            status=order.status.value,
            total_price=order.total_price,
            restaurant=OrderRestaurantOut.model_validate(order.restaurant),
            delivery_location=(
                OrderAddressOut.model_validate(order.delivery_location)
                if order.delivery_location
                else None
            ),
            items=items,
        )

    @staticmethod
    def _line_total(item) -> Decimal:
        """Compute the total for one order item after discount.

        The discount is treated as a percentage of the gross amount.

        Args:
            item: The OrderItem to calculate the total for.

        Returns:
            price * quantity minus discount percent.
        """
        gross = item.price * item.quantity
        return gross - (gross * Decimal(item.discount) / Decimal(100))

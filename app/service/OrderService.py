"""
This module provides service operations for managing customer orders and transactions.
"""

from decimal import Decimal
from fastapi import HTTPException, status
from tortoise.exceptions import IntegrityError
from tortoise.transactions import in_transaction

from app.models import Order, OrderItem, Item, Restraunt, Address, User
from app.schemas.orders import OrderCreate
from app.exception.AuthException import RestrauntNotFound, AddressNotFoundError


class OrderService:
    """Provides atomic business logic operations for processing order details."""

    @staticmethod
    async def create_order(data: OrderCreate, current_user: User) -> Order:
        """Process and persist a new customer order with item inventory checks using select_for_update.

        Args:
            data (OrderCreate): Validated Pydantic schema containing restaurant, location, and item lists.
            current_user (User): The authenticated active User database model instance making the purchase.

        Returns:
            Order: The fully populated and saved main Order database instance.

        Raises:
            HTTPException: 404 error if the specified restaurant or delivery location is invalid/missing.
            HTTPException: 404 error if an item ID does not exist or belong to the restaurant.
            HTTPException: 400 error if an item's requested quantity exceeds available stock.
            HTTPException: 409 conflict error if a database integrity lock or concurrency collision is tripped.
        """
        restaurant_exists = await Restraunt.filter(id=data.restaurant_id, is_active=True).exists()
        if not restaurant_exists:
            raise RestrauntNotFound()

        address_exists = await Address.filter(id=data.delivery_location_id, is_active=True).exists()
        if not address_exists:
            raise AddressNotFoundError()

        items=data.items.sort()
        try:
            async with in_transaction():
                total_order_price = Decimal("0.000")
                validated_items_list = []

                for order_item_data in items:
                    menu_item = await Item.filter(
                        id=order_item_data.item_id, 
                        restaurant_id=data.restaurant_id, 
                        is_active=True
                    ).select_for_update().first()

                    if not menu_item:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Menu item ID {order_item_data.item_id} is unavailable or doesn't belong to this restaurant.",
                        )

                    if menu_item.quantity < order_item_data.quantity:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Insufficient stock for item '{menu_item.item_name}'. Available: {menu_item.quantity}, Requested: {order_item_data.quantity}.",
                        )

                    menu_item.quantity -= order_item_data.quantity
                    await menu_item.save(update_fields=["quantity"])

                    item_total = Decimal(str(menu_item.price)) * Decimal(order_item_data.quantity)
                    total_order_price += item_total
                    validated_items_list.append((menu_item, order_item_data.quantity))

                order = await Order.create(
                    user=current_user,
                    restaurant_id=data.restaurant_id,
                    delivery_location_id=data.delivery_location_id,
                    total_price=total_order_price.quantize(Decimal('1.000')),
                    status="Pending",
                )
                for menu_item, quantity in validated_items_list:
                    await OrderItem.create(
                        order=order,
                        item=menu_item,
                        quantity=quantity,
                        price_at_purchase=menu_item.price
                    )

                return order

        except IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Order processing failed due to a structural database conflict or concurrent lock failure.",
            ) from exc

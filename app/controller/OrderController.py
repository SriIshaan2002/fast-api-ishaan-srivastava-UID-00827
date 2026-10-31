"""
This module provides operational API endpoints
for managing the customer order lifecycle.
"""

from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.dependency.dependency import get_active_user
from app.exception.AuthException import OrderNotFoundError
from app.models import User
from app.routes.OrderRouter import orderRouter
from app.schemas.orders import OrderCreate, OrderOut, OrderResponse
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
    try:
        return await OrderService.get_order(order_id, current_user.id)
    except OrderNotFoundError:
        raise HTTPException(status_code=404, detail="Order not found")

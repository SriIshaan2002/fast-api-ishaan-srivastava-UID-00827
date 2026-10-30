"""
This module provides operational API endpoints for managing the customer order lifecycle.
"""

from typing import Annotated
from fastapi import APIRouter, Depends, status

from app.dependency.dependency import get_active_user
from app.models import User
from app.schemas.orders import OrderCreate, OrderResponse
from app.service.OrderService import OrderService
from app.routes.OrderRouter import orderRouter

CurrentUser = Annotated[User, Depends(get_active_user)]


@orderRouter.post(
    "/", 
    response_model=OrderResponse, 
    status_code=status.HTTP_201_CREATED
)
async def create_order(
    payload: OrderCreate,
    current_user: CurrentUser,
):
    """Instantiate a brand-new restaurant order entry and track individual purchase line items.

    Args:
        payload (OrderCreate): Validated Pydantic schema detailing the restaurant targets and item counts.
        current_user (CurrentUser): The active authenticated User instance extracted from the security token.

    Returns:
        OrderResponse: The Pydantic-serialized JSON summary details of the successfully processed order.
    """
    return await OrderService.create_order(
        data=payload, 
        current_user=current_user
    )

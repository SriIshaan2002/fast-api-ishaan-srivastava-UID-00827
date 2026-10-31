"""Define Pydantic schemas for order creation and response validation."""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class OrderStatus(str, Enum):
    """Represent the possible statuses of a restaurant order."""

    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    PREPARING = "Preparing"
    ON_THE_WAY = "On-the-Way"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"
    RETURNED = "Returned"


class OrderItemCreate(BaseModel):
    """Validate an individual item included in a new order."""

    item_id: int
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    """Validate the data required to create a restaurant order."""

    restaurant_id: int
    delivery_location_id: int
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderResponse(BaseModel):
    """Represent the order details returned by the API."""

    model_config = ConfigDict(from_attributes=True)
    id: int
    restaurant_id: int
    total_price: Decimal
    status: OrderStatus
    created_at: datetime
    delivered_in: datetime | None = None


class OrderItemOut(BaseModel):
    """Schema representing an individual line
    item associated with an order."""

    model_config = ConfigDict(from_attributes=True)
    id: int
    item_name: str
    is_veg: bool
    quantity: int
    discount: int
    price: Decimal
    line_total: Decimal


class OrderAddressOut(BaseModel):
    """Schema representing the reference identifier
    for the delivery address."""

    model_config = ConfigDict(from_attributes=True)
    id: int


class OrderRestaurantOut(BaseModel):
    """Schema representing the reference identifier
    for the originating restaurant."""

    model_config = ConfigDict(from_attributes=True)
    id: int


class OrderOut(BaseModel):
    """Detailed summary payload schema representing
    a finalized order record response."""

    model_config = ConfigDict(from_attributes=True)
    id: int
    status: OrderStatus
    total_price: Decimal
    restaurant: OrderRestaurantOut
    delivery_location: Optional[OrderAddressOut] = None
    items: list[OrderItemOut]
    delivered_in: datetime | None = None

from datetime import datetime
from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field
class OrderStatus(str, Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    PREPARING = "Preparing"
    ON_THE_WAY = "On-the-Way"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"
    RETURNED = "Returned"

class OrderItemCreate(BaseModel):
    item_id: int
    quantity: int = Field(gt=0)

class OrderCreate(BaseModel):
    restaurant_id: int
    delivery_location_id: int
    items: list[OrderItemCreate] = Field(min_length=1)

class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    restaurant_id: int
    total_price: Decimal
    status: OrderStatus
    created_at: datetime
    delivered_in: datetime | None
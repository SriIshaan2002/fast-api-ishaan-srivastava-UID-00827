from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from enums import OrderStatus


class MenuItemStat(BaseModel):
    item_name: str
    times_ordered: int  # number of order lines containing the item
    total_quantity: int  # total units sold


class TopCustomer(BaseModel):
    user_id: int
    name: str
    order_count: int
    total_spent: Decimal


class OrderListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    total_price: Decimal
    status: OrderStatus
    created_at: datetime


class OrderPage(BaseModel):
    total: int
    page: int
    page_size: int
    results: list[OrderListItem]

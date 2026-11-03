"""
This module defines Pydantic validation schemas for managing restaurant menu items.
"""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ItemCreate(BaseModel):
    """Schema for adding a new item to a restaurant."""

    item_name: str = Field(min_length=2, max_length=50)
    restaurant_id: int = Field(
        description="The ID of the restaurant offering this item."
    )
    quantity: int = Field(default=0, ge=0)
    is_veg: bool
    description: str | None = Field(default=None, max_length=500)
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=3)


class ItemUpdate(BaseModel):
    """Schema for updating an item in a restaurant."""

    item_name: str | None = Field(default=None, min_length=2, max_length=50)
    quantity: int | None = Field(default=None, ge=0)
    is_veg: bool | None = None
    description: str | None = Field(default=None, max_length=500)
    price: Decimal | None = Field(default=None, gt=0, max_digits=10, decimal_places=3)


class ItemResponse(BaseModel):
    """Schema for responses from item APIs."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    item_name: str
    restaurant_id: int
    quantity: int
    is_veg: bool
    description: str | None
    price: Decimal
    is_active: bool

"""
This module defines Pydantic validation schemas for managing restaurant menu items.
"""

from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ItemBase(BaseModel):
    """Base fields shared across menu item operations."""

    item_name: str = Field(..., min_length=1, max_length=50)
    quantity: int = Field(default=0, ge=0)
    is_veg: bool
    description: Optional[str] = Field(None, max_length=500)
    price: Decimal = Field(..., gt=0, max_digits=10, decimal_places=3)


class ItemCreate(ItemBase):
    """Validate incoming payload parameters for creating a new menu item."""
    
    restaurant_id: int


class ItemUpdate(BaseModel):
    """Validate incoming optional attributes for shifting menu item data fields."""

    item_name: Optional[str] = Field(None, min_length=1, max_length=50)
    quantity: Optional[int] = Field(None, ge=0)
    is_veg: Optional[bool] = None
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[Decimal] = Field(None, gt=0, max_digits=10, decimal_places=3)


class ItemResponse(ItemBase):
    """Format outbound server responses representing structural menu item columns."""

    id: int
    restaurant_id: int
    created_by_id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

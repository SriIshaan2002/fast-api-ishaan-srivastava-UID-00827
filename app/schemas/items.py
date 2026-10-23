"""
This file contains Schemas related to Items.
"""
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

class ItemCreate(BaseModel):
    """
    This class hold the schema for adding a new item in restraunt.
    """
    item_name: str = Field(min_length=2, max_length=20)
    quantity: int = Field(ge=0)
    is_veg: bool
    description: str | None = Field(default=None, max_length=255)
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=3)

class ItemUpdate(BaseModel):
    """
    This class holds the schema for updating the item in Restraunt
    """
    quantity: int | None = Field(default=None, ge=0)
    is_veg: bool | None = None
    description: str | None = Field(default=None, max_length=255)
    price: Decimal | None = Field(default=None, gt=0, max_digits=10, decimal_places=3)

class ItemResponse(BaseModel):
    """
    This class holds the schema for response of item apis.
    """
    model_config = ConfigDict(from_attributes=True)
    id: int
    item_name: str
    quantity: int
    is_veg: bool
    description: str | None
    price: Decimal
    is_active: bool

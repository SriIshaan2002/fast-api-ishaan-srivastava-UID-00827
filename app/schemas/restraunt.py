from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RestrauntCreate(BaseModel):
    restaurant_name: str = Field(min_length=2, max_length=50)
    street: str = Field(
         validation_alias="address_line", min_length=3, max_length=255
    )
    city: str = Field(min_length=2, max_length=100)
    zip: str = Field(validation_alias="postal_code", min_length=4, max_length=12)
    house: str = Field(default="N/A", min_length=1, max_length=50)
    state: str = Field(min_length=2, max_length=100)
    country: str = Field(min_length=2, max_length=100)
    is_closed: bool = True


class RestrauntUpdate(BaseModel):
    restaurant_name: str | None = Field(default=None, min_length=2, max_length=50)
    location_id: int | None = Field(default=None, gt=0)
    is_closed: bool | None = None


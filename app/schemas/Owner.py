from pydantic import BaseModel, ConfigDict

from app.schemas.restraunt import RestaurantSummary


class OwnerCreate(BaseModel):
    """Schema for creating an owner."""

    user_id: int
    restraunt_id: int


class OwnerResponse(BaseModel):
    """Represent an owner-restaurant association."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    restraunt_id: int


class OwnerDetails(BaseModel):
    restaurants: list[RestaurantSummary]

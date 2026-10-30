from pydantic import BaseModel, ConfigDict, EmailStr, Field


class OwnerCreate(BaseModel):
    """Schema for creating an owner."""

    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    mobile: str = Field(min_length=10, max_length=13)
    password: str = Field(min_length=8, max_length=128)


class OwnerResponse(BaseModel):
    """Schema for returning owner details."""

    id: int
    name: str
    email: EmailStr
    mobile: str
    model_config = ConfigDict(from_attributes=True)

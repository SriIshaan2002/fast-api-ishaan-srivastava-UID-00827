from pydantic import BaseModel, ConfigDict, Field


class AddressCreate(BaseModel):
    """Schema for creating an address."""

    street: str = Field(validation_alias="address_line", min_length=3, max_length=255)
    city: str = Field(min_length=2, max_length=100)
    zip: str = Field(validation_alias="postal_code", min_length=4, max_length=12)
    house: str = Field(default="N/A", min_length=1, max_length=50)
    state: str = Field(min_length=2, max_length=100)
    country: str = Field(min_length=2, max_length=100)



class AddressUpdate(BaseModel):
    """Schema for updating address details."""

    address_line: str | None = Field(default=None, min_length=3, max_length=255)
    city: str | None = Field(default=None, min_length=2, max_length=100)
    state: str | None = Field(default=None, min_length=2, max_length=100)
    postal_code: str | None = Field(default=None, min_length=4, max_length=12)
    country: str | None = Field(default=None, min_length=2, max_length=100)


class AddressResponse(BaseModel):
    """Schema for returning address details."""

    id: int
    user_id: int
    city: str
    address_line: str = Field(
        validation_alias="street", serialization_alias="address_line"
    )
    postal_code: str = Field(validation_alias="zip", serialization_alias="postal_code")
    state: str = Field(default="N/A")
    country: str = Field(default="N/A")
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

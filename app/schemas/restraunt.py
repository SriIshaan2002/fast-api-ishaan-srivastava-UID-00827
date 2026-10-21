from pydantic import BaseModel, ConfigDict, Field

class RestaurantCreate(BaseModel):
    restaurant_name: str = Field(min_length=2, max_length=20)
    state: str = Field(max_length=15)
    city: str = Field(max_length=15)
    zip: str = Field(max_length=10)
    street: str = Field(max_length=50)
    nearby_location: str | None = Field(default=None, max_length=50)

class RestaurantUpdate(BaseModel):
    restaurant_name: str | None = Field(default=None, max_length=20)
    state: str | None = Field(default=None, max_length=15)
    city: str | None = Field(default=None, max_length=15)
    zip: str | None = Field(default=None, max_length=10)
    street: str | None = Field(default=None, max_length=50)
    nearby_location: str | None = Field(default=None, max_length=50)
    is_closed: bool | None = None

class RestaurantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    restaurant_name: str
    state: str
    city: str
    zip: str
    street: str
    is_closed: bool
    is_active: bool
"""Define Pydantic schemas for user creation, updates, login, and responses."""

from pydantic import BaseModel, EmailStr, Field, ConfigDict



class UserCreate(BaseModel):
    """Validate the data required to register a new user."""

    username: str = Field(min_length=5, max_length=20)
    password: str = Field(min_length=5, max_length=15)
    email: EmailStr


class UserResponse(BaseModel):
    """Represent user details returned by the API."""

    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    mobile: str
    email: EmailStr
    balance: Decimal
    is_active: bool
    created_at: datetime


class UserLogin(BaseModel):
    """Validate the credentials submitted when a user logs in."""

    email: str
    password: str

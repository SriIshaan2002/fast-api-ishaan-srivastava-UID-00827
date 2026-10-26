"""Define Pydantic schemas for user creation, updates, login, and responses."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """Validate the data required to register a new user."""

    username: str = Field(min_length=5, max_length=20)
    password: str = Field(min_length=5, max_length=15)
    email: EmailStr

class UserUpdate(BaseModel):
    """Validate optional fields for updating an existing user's profile."""
    username: str | None = Field(default=None, min_length=3, max_length=20)
    mobile: str | None = Field(default=None, min_length=10, max_length=13)
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=6, max_length=16)

class UserUpdate(BaseModel):
    """
    Validate optional fields for updating an existing user's profile.
    """

    username: str | None = Field(default=None, min_length=3, max_length=20)
    mobile: str | None = Field(default=None, min_length=10, max_length=13)
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=6, max_length=16)


class UserResponse(BaseModel):
    """Represent user details returned by the API."""

    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    mobile: str | None
    email: EmailStr
    balance: Decimal
    is_active: bool
    created_at: datetime
    model_config["from_attributes"] = True


class UserLogin(BaseModel):
    """Validate the credentials submitted when a user logs in."""

    email: str
    password: str

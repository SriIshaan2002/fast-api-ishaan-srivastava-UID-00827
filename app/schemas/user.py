"""Define Pydantic schemas for user creation, updates, login, and responses."""

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Validate the data required to register a new user."""

    username: str = Field(min_length=5, max_length=20)
    password: str = Field(min_length=5, max_length=15)
    email: EmailStr


class UserLogin(BaseModel):
    """Validate the credentials submitted when a user logs in."""

    email: str
    password: str

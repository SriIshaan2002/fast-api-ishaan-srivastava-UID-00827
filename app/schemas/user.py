from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    mobile: str = Field(min_length=10, max_length=13)
    email: EmailStr

class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=20)
    mobile: str | None = Field(default=None, min_length=10, max_length=13)
    email: EmailStr | None = None

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    mobile: str
    email: EmailStr
    balance: Decimal
    is_active: bool
    created_at: datetime
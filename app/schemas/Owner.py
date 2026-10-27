from pydantic import BaseModel, ConfigDict, EmailStr, Field


class OwnerCreate(BaseModel):
    """Schema for creating an owner."""
    user_id:int
    restraunt_id: int
    

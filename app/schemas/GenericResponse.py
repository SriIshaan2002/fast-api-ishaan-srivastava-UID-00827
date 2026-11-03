
from typing import Any

from pydantic import BaseModel, Field

class GenericResponse(BaseModel):
    """A generic response schema for API responses."""
    success: bool = Field(..., description="Indicates if the operation was successful.")
    message: str | None = Field(None, description="Optional message providing additional information.")
    data: Any | None = Field(None, description="Optional data content for the response.")

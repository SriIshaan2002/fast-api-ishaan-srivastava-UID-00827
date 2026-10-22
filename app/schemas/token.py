"""
Creating schema for the Login and Signup response contains access token and uuid of revoked at.
"""
from pydantic import BaseModel

class TokenResponse(BaseModel):
    """
    Response for Login and signup api
    """
    access_token: str | None
    user_uuid: str | None

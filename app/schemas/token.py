"""
Schemas for login and signup responses.

These schemas contain access token and token revocation information.
"""

from pydantic import BaseModel


class TokenResponse(BaseModel):
    """
    Response for Login and signup api
    """

    access_token: str | None
    user_uuid: str | None

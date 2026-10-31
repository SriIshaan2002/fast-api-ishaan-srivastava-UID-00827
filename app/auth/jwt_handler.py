"""JWT utilities for creating, decoding, and validating access and refresh tokens.

This module reads JWT configuration, defines the token payload model, and provides
helpers to create access tokens, create refresh tokens, and validate decoded
token payloads.
"""

import datetime
import uuid

import jwt
from pydantic import BaseModel, Field

from constants import AUTH_ERRORS
from db_config import jwt_config

SECRET_KEY = jwt_config.secret_key
ALGORITHM = jwt_config.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = jwt_config.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_DAYS = jwt_config.refresh_token_expire_days


class TokenPayload(BaseModel):
    """Represent and validate the payload contained in a JWT."""

    user_id: int
    is_admin: bool = False
    iat: int = Field(
        default_factory=lambda: int(datetime.datetime.now(datetime.UTC).timestamp())
    )
    exp: int
    type: str

    @property
    def is_expired(self) -> bool:
        return datetime.datetime.now(datetime.UTC).timestamp() > self.exp


def create_access_token(user_id: int, is_admin: bool) -> str:
    """Generates a short-lived access token for general API authorization.
        Validate a refresh token and generate a new access token.
    Args:
        user_id : unique id of user table
        is_admin : true/false

    Returns:
        JWT access token
    """
    iat = datetime.datetime.now(datetime.UTC)
    expire = iat + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    header = {"alg": ALGORITHM, "typ": "JWT"}
    payload = {
        "user_id": user_id,
        "is_admin": is_admin,
        "iat": int(iat.timestamp()),
        "exp": int(expire.timestamp()),
        "type": "access",
    }
    return jwt.encode(payload, headers=header, key=SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token() -> tuple[str, str]:
    """Generate a refresh token and its unique identifier.
        Validate a refresh token and generate a new access token.
    Returns:
        refresh-token UUID and expire time
    """
    token_uuid = str(uuid.uuid4())
    expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )
    return token_uuid, expire


def decode_and_verify_token(token: str, expected_type: str = "access") -> TokenPayload:
    """Decode and validate a JWT and check its expected token type.
        Validate a refresh token and generate a new access token.
    Args:
        token : JWT token
        expected_type : access
    Returns:
        Payload of the token.
    """
    try:
        if expected_type == "access":
            raw_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            payload_data = TokenPayload(**raw_payload)
            if payload_data.type != expected_type:
                raise jwt.InvalidTokenError(AUTH_ERRORS.invalid_token)
            return payload_data
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError(AUTH_ERRORS.invalid_token)
    except (jwt.InvalidTokenError, Exception) as e:
        raise jwt.InvalidTokenError(AUTH_ERRORS.exception.format(str(e)))

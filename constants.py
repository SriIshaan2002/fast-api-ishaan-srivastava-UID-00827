"""Define reusable constants for API responses and error messages."""

from fastapi import namedtuple

# Authentication errors
INVALID_CREDENTIALS = "Invalid email or password"
USER_NOT_FOUND = "User not found"
USER_ALREADY_EXISTS = "User already exists"
ACCOUNT_INACTIVE = "User account is inactive"
INVALID_TOKEN = "Invalid or expired token"
TOKEN_EXCEPTION="Exception{}"

GeneralMessages = namedtuple(
    "GeneralMessages",
    ["start_message", "access_forbidden", "internal_server_error", "access_token"],
)


GENERAL = GeneralMessages(
    start_message="API is working! Go to /docs for Swagger.",
    access_forbidden="You do not have permission to perform this action",
    internal_server_error="An unexpected error occurred",
    access_token="access_token",
)

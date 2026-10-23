"""
Created common String constants by the use of named tuple"""

from collections import namedtuple

AuthErrors = namedtuple(
    "AuthErrors",
    [
        "registered_email",
        "invalid_password",
        "invalid_credentials",
        "user_not_found",
        "user_already_exists",
        "user_inactive",
        "invalid_token",
        "exception",
    ],
)

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

AUTH_ERRORS=AuthErrors(
    registered_email="Email already registered"
    invalid_token="Token is eighter invalid or missing"
    invalid_credentials="Credentials are wrong"
    user_not_found="User is not found"
    user_already_exists="User already exist"
    user_inactive="User is inacive"
    invalid_token="Token is invalid"
    exception="Exception :{}"
)

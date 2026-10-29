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
        "not_active",
    ],
)

Exception_messages = namedtuple(
    "Exception_messages",
    [
        "registration_failed",
        "authentication_failed",
        "user_not_found",
        "InvalidPassword",
        "AccountInactive",
        "InvalidToken",
        "SessionNotFound",
    ],
)

AuthSuccess = namedtuple(
    "AuthSuccess",
    ["registered", "reactivated", "logged_out"],
)

GeneralMessages = namedtuple(
    "GeneralMessages",
    ["start_message", "access_forbidden", "internal_server_error", "access_token"],
)

AUTH_SUCCESS = AuthSuccess(
    registered="Successfully Registered",
    reactivated="Reactivated Successfully",
    logged_out="Logged out Successfully",
)

GENERAL = GeneralMessages(
    start_message="API is working! Go to /docs for Swagger.",
    access_forbidden="You do not have permission to perform this action",
    internal_server_error="An unexpected error occurred",
    access_token="access_token",
)

AUTH_ERRORS = AuthErrors(
    registered_email="Email already registered",
    invalid_token="Token is eighter invalid or missing",
    invalid_credentials="Credentials are wrong",
    user_not_found="User is not found",
    user_already_exists="User already exist",
    user_inactive="User is inacive",
    exception="Exception :{}",
    not_active="User provided is Inactive please try to reactivate the User",
    invalid_password="Password provided is invalid",
)

EXCEPTION_MESSAGES = Exception_messages(
    registration_failed="Registration failed",
    InvalidPassword="Authentication failed: Invalid credentials provided.",
    authentication_failed="Authentication failed: User account not found.",
    AccountInactive="Authentication failed: This account is currently deactivated.",
    InvalidToken="Session invalid: The provided refresh token is invalid or expired.",
    SessionNotFound="Logout failed: Session already logged out or tracking UUID is invalid.",
    user_not_found="User not found",
)

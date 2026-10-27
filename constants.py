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
RestaurantErrors = namedtuple(
    "RestaurantErrors", ["not_found", "already_exists", "closed"]
)
OrderErrors = namedtuple(
    "OrderErrors", ["not_found", "already_cancelled", "insufficient_balance"]
)
GeneralMessages = namedtuple(
    "GeneralMessages",
    ["start_message", "access_forbidden", "internal_server_error", "access_token"],
)
SuccessMessages = namedtuple(
    "SuccessMessages",
    [
        "user_created",
        "user_updated",
        "user_deleted",
        "login_successful",
        "order_created",
    ],
)

AUTH_ERRORS = AuthErrors(
    registered_email="Email is already Registered",
    invalid_password="Password is Invalid",
    invalid_credentials="Invalid email or password",
    user_not_found="User not found",
    user_already_exists="User already exists",
    user_inactive="User is inactive",
    invalid_token="Invalid or expired token",
    exception="Exception{}",
)

RESTAURANT_ERRORS = RestaurantErrors(
    not_found="Restaurant not found",
    already_exists="Restaurant already exists",
    closed="Restaurant is closed",
)

ORDER_ERRORS = OrderErrors(
    not_found="Order not found",
    already_cancelled="Order is already cancelled",
    insufficient_balance="Insufficient balance",
)

GENERAL = GeneralMessages(
    start_message="API is working! Go to /docs for Swagger.",
    access_forbidden="You do not have permission to perform this action",
    internal_server_error="An unexpected error occurred",
    access_token="access_token",
)

SUCCESS_MESSAGES = SuccessMessages(
    user_created="User created successfully",
    user_updated="User updated successfully",
    user_deleted="User deleted successfully",
    login_successful="Login successful",
    order_created="Order created successfully",
)

OwnerErrors = namedtuple(
    "OwnerErrors",
    ["not_found", "already_exists", "invalid_password"],
)

AddressErrors = namedtuple(
    "AddressErrors",
    ["not_found", "access_forbidden"],
)

OwnerSuccessMessages = namedtuple(
    "OwnerSuccessMessages",
    ["owner_created", "owner_updated", "owner_deleted"],
)

AddressSuccessMessages = namedtuple(
    "AddressSuccessMessages",
    ["address_created", "address_updated", "address_deleted"],
)


OWNER_ERRORS = OwnerErrors(
    not_found="Owner not found",
    already_exists="Owner already exists",
    invalid_password="Password is invalid",
)

ADDRESS_ERRORS = AddressErrors(
    not_found="Address not found",
    access_forbidden="You do not have permission to access this address",
)

OWNER_SUCCESS_MESSAGES = OwnerSuccessMessages(
    owner_created="Owner created successfully",
    owner_updated="Owner updated successfully",
    owner_deleted="Owner deleted successfully",
)

ADDRESS_SUCCESS_MESSAGES = AddressSuccessMessages(
    address_created="Address created successfully",
    address_updated="Address updated successfully",
    address_deleted="Address deleted successfully",
)

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
        "InternalServerError",
    ],
)

Restraunt_exceptions = namedtuple(
    "Restraunt_exceptions",
    ["Restraunt_not_found", "Restraunt_Already_exists", "Input_Unsatisfied"],
)

RESTRAUNT_EXCEPTIONS = Restraunt_exceptions(
    Restraunt_not_found="Restraunt Not found",
    Restraunt_Already_exists="Restraunt Already exists",
    Input_Unsatisfied="Input Not Satisfied",
)

Success = namedtuple("Success", ["Deleted"])
Success = namedtuple("Success", ["Deleted"])

SUCCESS_MESSAGES = Success(Deleted="User Deleted Successfully")

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
    SessionNotFound="Logout failed: "
    "Session already logged out or tracking UUID is invalid.",
    user_not_found="User not found",
    InternalServerError="Internal Server Error",
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

StatusConfig = namedtuple("StatusConfig", ["not_found", "bad_request", "conflict"])

OrderMessageConfig = namedtuple(
    "OrderMessageConfig",
    ["not_found", "empty", "conflict", "update_conflict", "insufficient_balance"],
)

ItemMessageConfig = namedtuple(
    "ItemMessageConfig",
    [
        "invalid_quantity",
        "not_found_restaurant",
        "not_found_generic",
        "update_empty",
        "insufficient_stock",
    ],
)

DatabaseMessageConfig = namedtuple("DatabaseMessageConfig", ["conflict"])

ORDER_MSG = OrderMessageConfig(
    not_found="Order {order_id} not found.",
    empty="An order must contain at least one item.",
    conflict="Order processing failed due to a "
    "database conflict or lock failure. Please retry.",
    update_conflict="Order update failed due to a "
    "database conflict or lock failure. Please retry.",
    insufficient_balance="Order total exceeds your balance.",
)

ITEM_MSG = ItemMessageConfig(
    invalid_quantity="Quantity for item {item_id} must be greater than 0.",
    not_found_restaurant="Menu item ID {item_id} is unavailable or"
    " doesn't belong to this restaurant.",
    not_found_generic="The requested menu item could not be found or is inactive.",
    update_empty="No structural update parameters were supplied.",
    insufficient_stock="Insufficient stock for item '{item_name}'."
    "Available: {available}, Requested: {requested}.",
)

DB_MSG = DatabaseMessageConfig(
    conflict="Failed to finalize database operations due"
    " to a structural backend layout conflict."
)

MiddlewareMessages = namedtuple(
    "MiddlewareMessages",
    ["Success", "Failed"],
)

MIDDLEWARE_MESSAGES = MiddlewareMessages(
    Success="Request processed successfully",
    Failed="Request failed"
)

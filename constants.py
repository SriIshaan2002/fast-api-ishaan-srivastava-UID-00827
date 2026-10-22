"""Define reusable constants for API responses and error messages."""

# Authentication errors
INVALID_CREDENTIALS = "Invalid email or password"
USER_NOT_FOUND = "User not found"
USER_ALREADY_EXISTS = "User already exists"
ACCOUNT_INACTIVE = "User account is inactive"
INVALID_TOKEN = "Invalid or expired token"
TOKEN_EXCEPTION="Exception{}"

# Restaurant errors
RESTAURANT_NOT_FOUND = "Restaurant not found"
RESTAURANT_ALREADY_EXISTS = "Restaurant already exists"
RESTAURANT_CLOSED = "Restaurant is closed"

# Order errors
ORDER_NOT_FOUND = "Order not found"
ORDER_ALREADY_CANCELLED = "Order is already cancelled"
INSUFFICIENT_BALANCE = "Insufficient balance"

# General errors
ACCESS_FORBIDDEN = "You do not have permission to perform this action"
INTERNAL_SERVER_ERROR = "An unexpected error occurred"

# Success messages
USER_CREATED = "User created successfully"
USER_UPDATED = "User updated successfully"
LOGIN_SUCCESSFUL = "Login successful"
ORDER_CREATED = "Order created successfully"

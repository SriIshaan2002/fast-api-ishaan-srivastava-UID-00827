"""Define reusable constants for API responses and error messages."""
START_MESSAGE="API is working! Go to /docs for Swagger."

# Authentication errors
REGISTERED_EMAIL="Email is already Registered"
INVALID_PASSWORD="Password is Invalid"
INVALID_CREDENTIALS = "Invalid email or password"
USER_NOT_FOUND = "User not found"
USER_ALREADY_EXISTS = "User already exists"
USER_INACTIVE = "User is inactive"
INVALID_TOKEN = "Invalid or expired token"
EXCEPTION="Exception{}"

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
USER_DELETED = "User deleted successfilly"
LOGIN_SUCCESSFUL = "Login successful"
ORDER_CREATED = "Order created successfully"

#Non success message
USER_NOT_FOUND="User not found"

ACCESS_TOKEN="access_token"

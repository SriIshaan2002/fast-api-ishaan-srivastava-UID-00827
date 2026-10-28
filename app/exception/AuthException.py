from app.exception import CustomBaseException


class RegistrationError(CustomBaseException):
    """Represent an authentication-related signup error."""

    status_code = 409

    def __init__(self, error: str = "Registration failed"):
        formatted_detail = f"Cannot Register User: {error}"
        super().__init__(status_code=self.status_code, detail=formatted_detail)


class UserNotFoundError(CustomBaseException):
    status_code = 404
    detail = "Authentication failed: User account not found."


class InvalidPasswordError(CustomBaseException):
    status_code = 401
    detail = "Authentication failed: Invalid credentials provided."


class AccountInactiveError(CustomBaseException):
    status_code = 403
    detail = "Authentication failed: This account is currently deactivated."


class InvalidTokenError(CustomBaseException):
    status_code = 401
    detail = "Session invalid: The provided refresh token is invalid or expired."


class SessionNotFoundError(CustomBaseException):
    status_code = 404
    detail = "Logout failed: Session already logged out or tracking UUID is invalid."


class ReactivationFailedError(CustomBaseException):
    status_code = 400

    def __init__(self, reason: str):
        formatted_detail = f"Reactivation failed: {reason}"
        super().__init__(status_code=self.status_code, detail=formatted_detail)

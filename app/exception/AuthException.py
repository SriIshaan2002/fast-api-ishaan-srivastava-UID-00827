"""This module is about making custom exception"""

from fastapi import status

from app.exception.BaseException import CustomBaseException
from constants import EXCEPTION_MESSAGES


class RegisteredEmail(CustomBaseException):
    """Represent an authentication-related signup error."""

    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, error: str = "Registration failed"):
        formatted_detail = error
        super().__init__(status_code=self.status_code, detail=formatted_detail)


class UserNotFoundError(CustomBaseException):
    """Represent an User not found error."""

    status_code = status.HTTP_404_NOT_FOUND
    detail = EXCEPTION_MESSAGES.user_not_found


class InvalidPasswordError(CustomBaseException):
    """Represent an Invalid Password error."""

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = EXCEPTION_MESSAGES.InvalidPassword


class AccountInactiveError(CustomBaseException):
    """Represent an Account Inactive error."""

    status_code = status.HTTP_403_FORBIDDEN
    detail = EXCEPTION_MESSAGES.AccountInactive


class InvalidTokenError(CustomBaseException):
    """Represent an Invalid Token error."""

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = EXCEPTION_MESSAGES.InvalidToken


class SessionNotFoundError(CustomBaseException):
    """Represent an Session not found error."""

    status_code = status.HTTP_404_NOT_FOUND
    detail = EXCEPTION_MESSAGES.SessionNotFound


class ReactivationFailedError(CustomBaseException):
    """Represent an Reactivation Failed error."""

    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, reason: str):
        formatted_detail = f"Reactivation failed: {reason}"
        super().__init__(status_code=self.status_code, detail=formatted_detail)

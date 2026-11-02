"""This module is about making custom exception"""

from fastapi import status

from app.exception.BaseException import CustomBaseException
from constants import (
    ADDRESS_ERRORS,
    DB_MSG,
    EXCEPTION_MESSAGES,
    ITEM_MSG,
    ORDER_MSG,
    OWNER_ERRORS,
    RESTRAUNT_EXCEPTIONS,
)


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


class AddressNotFoundError(CustomBaseException):
    """Raised when an address does not exist or is inaccessible."""

    def __init__(self):
        super().__init__(
            detail=ADDRESS_ERRORS.not_found,
            status_code=status.HTTP_404_NOT_FOUND,
        )


class OwnerAlreadyExistsError(CustomBaseException):
    """Raised when an owner already exists."""

    detail = OWNER_ERRORS.already_exists
    status_code = status.HTTP_409_CONFLICT


class RestrauntNotFound(CustomBaseException):
    """Raised when an owner already exists."""

    detail = RESTRAUNT_EXCEPTIONS.Restraunt_not_found
    status_code = status.HTTP_404_NOT_FOUND


class OwnerNotFound(CustomBaseException):
    """Raised when an owner already exists."""

    detail = OWNER_ERRORS.not_found
    status_code = status.HTTP_404_NOT_FOUND


class RestaurantAlreadyExists(CustomBaseException):
    """Raised when an operations
    violation hits a unique restaurant constraint."""

    detail = RESTRAUNT_EXCEPTIONS.Restraunt_Already_exists
    status_code = status.HTTP_409_CONFLICT


class InvalidRestaurantInput(CustomBaseException):
    """Raised when input schemas
    are unsatisfied or completely empty."""

    detail = RESTRAUNT_EXCEPTIONS.Input_Unsatisfied
    status_code = status.HTTP_400_BAD_REQUEST


class InvalidLocationInput(CustomBaseException):
    """Raised when trying to provide
    an invalid or null location value."""

    detail = ADDRESS_ERRORS.not_found
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


class OrderNotFoundError(CustomBaseException):
    """Raised when an order doesn't exist or doesn't belong to the user."""

    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, order_id: int):
        self.order_id = order_id
        super().__init__(ORDER_MSG.NOT_FOUND.format(order_id=order_id))


class OrderEmptyError(CustomBaseException):
    """Raised when an order is placed with no items."""

    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self):
        super().__init__(ORDER_MSG.EMPTY)


class InvalidQuantityError(CustomBaseException):
    """Raised when a requested quantity is zero or negative."""

    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, item_id: int):
        self.item_id = item_id
        super().__init__(ITEM_MSG.INVALID_QUANTITY.format(item_id=item_id))


class ItemNotFoundError(CustomBaseException):
    """Raised when an item is missing, inactive, or not in the restaurant."""

    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, item_id: int):
        self.item_id = item_id
        super().__init__(ITEM_MSG.NOT_FOUND_RESTAURANT.format(item_id=item_id))


class InsufficientStockError(CustomBaseException):
    """Raised when a requested quantity exceeds available stock."""

    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, item_name: str, available: int, requested: int):
        self.item_name = item_name
        self.available = available
        self.requested = requested
        super().__init__(
            ITEM_MSG.INSUFFICIENT_STOCK.format(
                item_name=item_name, available=available, requested=requested
            )
        )


class OrderConflictError(CustomBaseException):
    """Raised on a database integrity
    error or lock/deadlock failure."""

    status_code = status.HTTP_409_CONFLICT

    def __init__(self):
        super().__init__(ORDER_MSG.CONFLICT)


class ItemNotFound(CustomBaseException):
    """Raised when a target menu item lookup
    fails or has been soft-deleted."""

    status_code = status.HTTP_404_NOT_FOUND
    detail = ITEM_MSG.not_found_generic


class ItemUpdateEmpty(CustomBaseException):
    """Raised when an update request payload
    contains no modifications."""

    status_code = status.HTTP_400_BAD_REQUEST
    detail = ITEM_MSG.update_empty


class DatabaseConflictException(CustomBaseException):
    """Raised when a unique constraint or structural
    validation rule fails in the engine."""

    status_code = status.HTTP_409_CONFLICT
    detail = DB_MSG.conflict

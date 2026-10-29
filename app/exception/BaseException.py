"""This module define a base class for all the xustome exceptions"""

from constants import GENERAL


class CustomBaseException(Exception):
    """Base class for all custom application errors with default fallbacks."""

    status_code: int = 500
    detail: str = GENERAL.internal_server_error

    def __init__(self, status_code: int = None, detail: str = None):
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = detail

        super().__init__(self.detail)

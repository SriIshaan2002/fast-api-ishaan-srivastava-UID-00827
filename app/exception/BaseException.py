class CustomBaseException(Exception):
    """Base class for all custom application errors with default fallbacks."""
    status_code: int = 500
    detail: str = "An unexpected server error occurred."

    def __init__(self, status_code: int = None, detail: str = None):
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = detail
            
        super().__init__(self.detail)

"""
This module is Handling the Exception missed
This ia a global exception handler
"""

from fastapi import FastAPI, requests, status
from fastapi.responses import JSONResponse


def global_handler(app: FastAPI) -> None:
    """
    This function accepts the exception returns a normal JSon response with the
    exception detail in the body
    """

    @app.exception_handler(Exception)
    async def handler(request: requests, exc: Exception) -> JSONResponse:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={str(exc)})

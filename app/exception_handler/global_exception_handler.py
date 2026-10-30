"""
This module provides global exception middleware
handling to capture unhandled runtime errors.
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.exception.BaseException import CustomBaseException
from constants import EXCEPTION_MESSAGES


def global_handler(app: FastAPI) -> None:
    """Register a catch-all global exception
    handler wrapper onto the FastAPI application instance.

    Args:
        app (FastAPI): The root or sub-mounted
        FastAPI application instance to bind the handler to.
    """

    @app.exception_handler(CustomBaseException)
    async def custom_handler(
        request: Request,
        exc: CustomBaseException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(Exception)
    async def handler(request: Request, exc: Exception) -> JSONResponse:
        """Intercept unhandled application exceptions
        and transform them into unified JSON responses.

        Args:
            request (Request): The incoming Starlette/FastAPI request object context.
            exc (Exception): The raw unhandled
            Python exception instance intercepted by the engine.

        Returns:
            JSONResponse: A serialized JSON
            body containing error details with a 500 status code.
        """
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": EXCEPTION_MESSAGES.InternalServerError},
        )

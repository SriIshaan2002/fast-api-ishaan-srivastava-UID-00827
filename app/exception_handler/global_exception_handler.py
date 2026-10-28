from fastapi import FastAPI, requests, status
from fastapi.responses import JSONResponse


def global_handler(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def handler(request: requests, exc: Exception) -> JSONResponse:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={str(exc)})

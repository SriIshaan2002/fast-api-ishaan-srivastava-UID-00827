import json

from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.schemas.GenericResponse import GenericResponse
from constants import MIDDLEWARE_MESSAGES

SKIP_PATHS = {"/docs", "/redoc", "/openapi.json"}


async def response_interceptor(request: Request, call_next):
    """Intercepts outgoing responses to wrap them in a consistent format."""
    if request.url.path in SKIP_PATHS:
        return await call_next(request)
    try:
        response = await call_next(request)
    except Exception as e:
        return JSONResponse(
            content=GenericResponse(
                success=False, message=MIDDLEWARE_MESSAGES.InternalError, data=str(e)
            ).model_dump(mode="json"),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    chunks = []
    async for chunk in response.body_iterator:
        chunks.append(chunk)
    body = b"".join(chunks)
    data = json.loads(body.decode("utf-8")) if body else None
    ok = response.status_code < 400
    wrapped = GenericResponse(
        success=ok,
        message=MIDDLEWARE_MESSAGES.Success if ok else MIDDLEWARE_MESSAGES.Failed,
        data=data,
    ).model_dump(mode="json")

    return JSONResponse(content=wrapped, status_code=response.status_code)

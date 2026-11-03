from fastapi import Request
import json

from app.schemas.GenericResponse import GenericResponse
from fastapi.responses import JSONResponse
from constants import MIDDLEWARE_MESSAGES

SKIP_PATHS = {"/docs", "/redoc", "/openapi.json"}

async def response_interceptor(request: Request, call_next):
    response = await call_next(request)

    content_type = response.headers.get("content-type", "")
    if request.url.path in SKIP_PATHS or not content_type.startswith("application/json"):
        return response

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
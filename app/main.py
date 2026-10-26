import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from constants import GENERAL
import settings
from app.controller.UserController import routerAdmin, routerUser

app = FastAPI(title="My First FastAPI Template")

app.include_router(routerUser)
app.include_router(routerAdmin)
# Plug in the user routes under the "/api" prefix
# app.include_router(user_router, prefix="/api")

register_tortoise(
    app,
    config=settings.TORTOISE_ORM,  # Uses your exact PostgreSQL configuration
    add_exception_handlers=True,
)


@app.get("/")
def index():
    return {"message": GENERAL.start_message}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

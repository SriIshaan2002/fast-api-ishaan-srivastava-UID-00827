import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

import settings
import app.routes.AuthRouter
import app.routes.AdminRoutes
import app.routes.OwnerRoutes
import app.routes.UserRouter
import app.routes.AddressRoutes

from app.routes import (
    authRouter,
    routerAdmin,
    routerOwner,
    routerUser,
    routerAdress,
)
from app.middleware.auth import unified_auth_middleware
from constants import GENERAL
from app.exception_handler import global_handler

app = FastAPI(title="My First FastAPI Template")

app.middleware("http")(unified_auth_middleware)

app.include_router(authRouter)
app.include_router(routerUser)
app.include_router(routerAdmin)
app.include_router(routerAdress)
app.include_router(routerOwner)

print("Auth router routes:", authRouter.routes)

app.include_router(authRouter)

print("Application routes:", app.routes)
global_handler(app)
app.middleware("http")(unified_auth_middleware)

register_tortoise(
    app,
    config=settings.TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.get("/")
def index():
    return {"message": GENERAL.start_message}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

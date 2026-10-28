import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

import settings
from app.middleware.auth import unified_auth_middleware
from app.routes.AddressController import router as addressRouter
from app.routes.auth import authRouter
from app.routes.OwnerController import router as ownerRouter
from app.routes.UserController import routerAdmin, routerUser
from constants import GENERAL

app = FastAPI(title="My First FastAPI Template")

app.middleware("http")(unified_auth_middleware)

app.include_router(authRouter)
app.include_router(routerUser)
app.include_router(routerAdmin)
app.include_router(addressRouter)
app.include_router(ownerRouter)
# Plug in the user routes under the "/api" prefix
# app.include_router(user_router, prefix="/api")

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

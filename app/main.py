import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

import settings
from app.controller.AddressController import routerAdress as addressRouter
from app.controller.AuthController import authRouter
from app.controller.OwnerController import routerOwner as ownerRouter
from app.controller.UserController import routerAdmin, routerUser
from app.controller.OrderController import orderRouter
from app.controller.RestrauntController import restaurant_router
from app.middleware.auth import unified_auth_middleware
from constants import GENERAL

app = FastAPI(title="My First FastAPI Template")

app.middleware("http")(unified_auth_middleware)

app.include_router(authRouter)
app.include_router(routerUser)
app.include_router(routerAdmin)
app.include_router(addressRouter)
app.include_router(ownerRouter)
app.include_router(orderRouter)
app.include_router(restaurant_router)
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

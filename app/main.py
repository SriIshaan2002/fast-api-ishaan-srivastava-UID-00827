import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

import settings
from app.controller.AddressController import routerAdress
from app.controller.AuthController import authRouter
from app.controller.ItemController import routerItems
from app.controller.OrderController import orderRouter
from app.controller.OwnerController import routerOwner
from app.controller.RestrauntController import restaurant_router
from app.controller.UserController import routerAdmin as userAdmin
from app.controller.UserController import routerUser as routerUser
from app.controller.StatsController import router
from app.exception_handler import global_handler
from app.middleware.auth import unified_auth_middleware
from constants import GENERAL

app = FastAPI(title="My First FastAPI Template")

app.middleware("http")(unified_auth_middleware)

app.include_router(authRouter)
app.include_router(routerUser)
app.include_router(userAdmin)
app.include_router(routerAdress)
app.include_router(routerOwner)
app.include_router(restaurant_router)
app.include_router(routerItems)
app.include_router(orderRouter)
app.include_router(router)

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

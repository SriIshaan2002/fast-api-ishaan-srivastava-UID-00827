import uvicorn
from fastapi import FastAPI
from app.routes.auth import authRouter
from app.routes.UserController import routerUser,routerAdmin
from tortoise.contrib.fastapi import register_tortoise
import settings
import constants as const

app = FastAPI(title="My First FastAPI Template")

app.include_router(authRouter) 
app.include_router(routerUser) 
app.include_router(routerAdmin) 
# Plug in the user routes under the "/api" prefix
#app.include_router(user_router, prefix="/api")

register_tortoise(
    app,
    config=settings.TORTOISE_ORM, # Uses your exact PostgreSQL configuration
    generate_schemas=True,         # Automatically sets up tables if they don't exist
    add_exception_handlers=True,
)

@app.get("/")
def index():
    return {"message": const.START_MESSAGE}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

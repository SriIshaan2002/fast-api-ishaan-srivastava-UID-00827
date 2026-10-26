import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

import settings
from app.routes.auth import authRouter
from constants import GENERAL

app = FastAPI(title="My First FastAPI Template")

app.include_router(authRouter, prefix="/auth", tags=["Authentication"])
app.include_router(routerUser)
app.include_router(routerAdmin)

register_tortoise(
    app,
    config=settings.TORTOISE_ORM,
    add_exception_handlers=True,
)


@app.get("/")
def index():
    return {"message": GENERAL.start_message}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

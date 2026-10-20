import uvicorn
from fastapi import FastAPI
#from app.api.users import router as user_router

app = FastAPI(title="My First FastAPI Template")

# Plug in the user routes under the "/api" prefix
#app.include_router(user_router, prefix="/api")

@app.get("/")
def index():
    return {"message": "API is working! Go to /docs for Swagger."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
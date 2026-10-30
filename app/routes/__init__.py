from fastapi import APIRouter

authRouter = APIRouter(prefix="/auth", tags=["Authentication"])
routerAdmin = APIRouter(prefix="/admin", tags=["Admin"])
routerOwner = APIRouter(prefix="/owner", tags=["Owner"])
routerUser = APIRouter(prefix="/user", tags=["User"])
routerAdress = APIRouter(prefix="/address", tags=["Address"])
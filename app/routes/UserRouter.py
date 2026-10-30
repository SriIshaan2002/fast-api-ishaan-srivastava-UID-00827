from fastapi import APIRouter, Depends

from app.dependency.dependency import get_active_user

routerUser = APIRouter(
    prefix="/users",
    tags=["User Management"],
    dependencies=[Depends(get_active_user)],
)

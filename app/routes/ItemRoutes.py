from fastapi import APIRouter, Depends
from app.dependency.dependency import get_active_user

routerItems = APIRouter(prefix="/items", tags=["Menu Items"], dependencies=[Depends(get_active_user)])

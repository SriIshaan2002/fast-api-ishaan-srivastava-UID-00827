from fastapi import APIRouter, Depends
from app.dependency.dependency import get_active_user

restaurant_router = APIRouter(
    prefix="/restaurants", tags=["Restaurants"], dependencies=[Depends(get_active_user)]
)

from app.models import User
from FastAPI import APIRouter, HTTPException
from app.schemas import UserCreate, UserUpdate, UserResponse

routerAdmin = APIRouter(tags=["User Management ADMIN"], prefix="/users")
routerUser = APIRouter(tags=["User Management"], prefix="/users")
@routerAdmin.get("/")
async def get_users():
    users = await User.all()
    return users

@routerAdmin.get("/{user_id}")
async def get_user(user_id: int):
    user = await User.get_or_none(user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@routerUser.post("/")
async def create_user(user: UserCreate):
    user = await User.create(**user.dict())
    return UserResponse

@routerUser.delete("/{user_id}")
async def delete_user(user_id: int):
    user = await User.get_or_none(user_id=user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=404, detail="User not found")
    await user.update_from_dict({"is_active": False}).save()
    return {"message": "User deleted successfully"}

@routerUser.put("/{user_id}")
async def update_user(user_id: int, user: UserUpdate):
    existing_user = await User.get_or_none(user_id=user_id)
    if not existing_user or not existing_user.is_active :
        raise HTTPException(status_code=404, detail="User not found")
    await existing_user.update_from_dict(user.dict()).save()
    return existing_user


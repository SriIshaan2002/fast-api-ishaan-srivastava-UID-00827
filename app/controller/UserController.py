from app.models import User
from FastAPI import APIRouter, HTTPException

router = APIRouter(tags=["User Management"], prefix="/users")

@router.get("/")
async def get_users():
    users = await User.all()
    return users
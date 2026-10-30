from fastapi import APIRouter, Depends
from app.dependency.dependency import get_active_user
from app.models.model import User
from app.exception.AuthException import AccountInactiveError

async def require_admin(current_user: User = Depends(get_active_user)) -> User:
    """Allow access only to authenticated administrators.

    Args:
        current_user (User): The active authenticated
        User instance from dependency injection.

    Returns:
        User: The authenticated administrator instance.

    Raises:
        HTTPException: 403 error if the
        authenticated user lacks admin privileges.
    """
    if not current_user.is_admin:
        raise AccountInactiveError
    return current_user


routerAdmin = APIRouter(
    prefix="/admin",
    tags=["User Management ADMIN"],
    dependencies=[Depends(require_admin)],
)
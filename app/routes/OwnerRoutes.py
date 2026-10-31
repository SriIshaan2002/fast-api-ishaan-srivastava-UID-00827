from fastapi import APIRouter, Depends

from app.dependency.dependency import get_active_user
from app.exception.AuthException import AccountInactiveError
from app.models.model import User


async def require_Admin(current_user: User = Depends(get_active_user)) -> User:
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


routerOwner = APIRouter(
    prefix="/admin/owner",
    tags=["Owner APIs for Admin"],
    dependencies=[Depends(require_Admin)],
)

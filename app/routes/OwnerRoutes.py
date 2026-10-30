from fastapi import APIRouter, Depends
from app.dependency.dependency import get_active_user
from app.models.model import User, Owner
from app.exception.AuthException import AccountInactiveError
from app.service.OwnerService import OwnerService

async def require_owner(current_user: User = Depends(get_active_user)) -> Owner:
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
    owner:Owner=OwnerService.get_owner(owner_id=User.id)
    return owner

routerOwner = APIRouter(
    prefix="/admin",
    tags=["User Management ADMIN"],
    dependencies=[Depends(require_owner)],
)
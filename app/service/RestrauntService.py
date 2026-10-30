from fastapi import HTTPException, status
from tortoise.exceptions import IntegrityError
from tortoise.transactions import in_transaction

from app.models import Address, Owner, Restraunt, User
from app.schemas.restraunt import RestrauntCreate, RestrauntResponse
from app.schemas.address import AddressCreate
from app.service.AddressService import AddressService
from constants import ADDRESS_ERRORS, GENERAL, RESTRAUNT_EXCEPTIONS
from app.exception.AuthException import AddressNotFoundError, RestrauntNotFound


def restraunt_to_dict(restraunt: Restraunt) -> dict:
    """Convert a restraunt model into a response-compatible dictionary."""
    return {
        "id": restraunt.id,
        "restraunt_name": restraunt.restraunt_name,
        "location_id": restraunt.location_id_id,
        "created_by_id": restraunt.created_by_id,
        "is_closed": restraunt.is_closed,
        "is_active": restraunt.is_active,
        "created_at": restraunt.created_at,
        "updated_at": restraunt.updated_at,
    }


async def get_active_address(address_id: int) -> Address:
    """Fetch an active address by ID."""
    try:
        address = await Address.filter(id=address_id, is_active=True).first()
    except Exception as e:
        raise e
    if address is None:
        raise AddressNotFoundError()
    return address


async def check_restraunt_access(restraunt: Restraunt, current_user: User) -> None:
    """Verify that the user is an administrator or restraunt owner."""
    if current_user.is_admin:
        return
    is_owner = await Owner.filter(
        user=current_user,
        restraunt=restraunt,
        is_active=True,
    ).exists()
    if not is_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=GENERAL.access_forbidden,
        )


async def create_restraunt(
    payload: RestrauntCreate,
    current_user: User,
) -> dict:
    """Create a restraunt and associate its creator as an owner."""

    try:
        async with in_transaction():
            address = await AddressService.create_address(
                data=AddressCreate(
                    address_line=payload.street,
                    city=payload.city,
                    postal_code=payload.zip,
                    state=payload.state,
                    country=payload.country,
                    house=payload.house,
                ),
                user_id=current_user.id,
            )
            restraunt = await Restraunt.create(
                restraunt_name=payload.restraunt_name,
                location_id=address,
                created_by=current_user,
                updated_by=current_user,
                is_closed=payload.is_closed,
            )
            await Owner.create(
                user=current_user,
                restraunt=restraunt,
                updated_by=current_user,
            )
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=RESTRAUNT_EXCEPTIONS.already_exists,
        ) from exc
    return restraunt_to_dict(restraunt)


async def get_restraunts() -> list[dict]:
    """Return all active restraunts."""

    restraunts = await Restraunt.filter(
        is_active=True,
    ).order_by("id")
    return [restraunt_to_dict(restraunt) for restraunt in restraunts]


async def get_restraunt(restraunt_id: int) -> dict:
    """Fetch an active restraunt by ID."""
    restraunt = await Restraunt.filter(
        id=restraunt_id,
        is_active=True,
    ).first()
    if restraunt is None:
        raise RestrauntNotFound()
    return restraunt_to_dict(restraunt)


async def update_restraunt(
    restraunt_id: int,
    payload: RestrauntResponse,
    current_user: User,
) -> dict:
    """Update an active restraunt after checking ownership."""
    restraunt = await Restraunt.filter(
        id=restraunt_id,
        is_active=True,
    ).first()
    if restraunt is None:
        raise RestrauntNotFound
    await check_restraunt_access(restraunt, current_user)
    update_data = payload.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=RESTRAUNT_EXCEPTIONS.Input_not_satisfied,
        )
    if "restraunt_name" in update_data and update_data["restraunt_name"] is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=RESTRAUNT_EXCEPTIONS.name_not_null,
        )
    if "location_id" in update_data:
        address_id = update_data.pop("location_id")
        if address_id is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=ADDRESS_ERRORS.cannot_be_null,
            )
        restraunt.location_id = await get_active_address(address_id)
    for field, value in update_data.items():
        setattr(restraunt, field, value)
    restraunt.updated_by = current_user
    try:
        await restraunt.save()
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=RESTRAUNT_EXCEPTIONS.already_exists,
        ) from exc
    return restraunt_to_dict(restraunt)


async def delete_restraunt(
    restraunt_id: int,
    current_user: User,
) -> None:
    """Soft-delete an active restraunt."""
    restraunt = await Restraunt.filter(id=restraunt_id, is_active=True).first()
    if restraunt is None:
        raise RestrauntNotFound()
    await check_restraunt_access(restraunt, current_user)
    restraunt.is_active = False
    restraunt.updated_by = current_user
    await restraunt.save(update_fields=["is_active", "updated_by", "updated_at"])

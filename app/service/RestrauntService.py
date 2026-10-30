from fastapi import HTTPException, status
from tortoise.exceptions import IntegrityError
from tortoise.transactions import in_transaction

from app.models import Address, Owner, Restraunt, User
from app.schemas import RestrauntCreate, RestrauntResponse
from app.schemas.address import AddressCreate
from app.service.AddressService import AddressService
from constants import ADDRESS_ERRORS, GENERAL, RESTRAUNT_EXCEPTIONS
from app.exception import RestrauntNotFound, AddressNotFoundError


def restaurant_to_dict(restaurant: Restraunt) -> dict:
    """Convert a restaurant model into a response-compatible dictionary."""
    return {
        "id": restaurant.id,
        "restaurant_name": restaurant.restaurant_name,
        "location_id": restaurant.location_id_id,
        "created_by_id": restaurant.created_by_id,
        "is_closed": restaurant.is_closed,
        "is_active": restaurant.is_active,
        "created_at": restaurant.created_at,
        "updated_at": restaurant.updated_at,
    }


async def get_active_address(address_id: int) -> Address:
    """Fetch an active address by ID."""
    try:
        address = await Address.filter(id=address_id, is_active=True).first()
    except Exception as e:
        raise e
    if address is None:
        raise RestrauntNotFound
    return address


async def check_restaurant_access(restaurant: Restraunt, current_user: User) -> None:
    """Verify that the user is an administrator or restaurant owner."""
    if current_user.is_admin:
        return
    is_owner = await Owner.filter(
        user=current_user,
        restraunt=restaurant,
        is_active=True,
    ).exists()
    if not is_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=GENERAL.access_forbidden,
        )


async def create_restaurant(
    payload: RestrauntCreate,
    current_user: User,
) -> dict:
    """Create a restaurant and associate its creator as an owner."""

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
            restaurant = await Restraunt.create(
                restaurant_name=payload.restaurant_name,
                location_id=address,
                created_by=current_user,
                updated_by=current_user,
                is_closed=payload.is_closed,
            )
            await Owner.create(
                user=current_user,
                restraunt=restaurant,
                updated_by=current_user,
            )
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=RESTRAUNT_EXCEPTIONS.already_exists,
        ) from exc
    return restaurant_to_dict(restaurant)


async def get_restaurants() -> list[dict]:
    """Return all active restaurants."""

    restaurants = await Restraunt.filter(
        is_active=True,
    ).order_by("id")
    return [restaurant_to_dict(restaurant) for restaurant in restaurants]


async def get_restaurant(restaurant_id: int) -> dict:
    """Fetch an active restaurant by ID."""
    restaurant = await Restraunt.filter(
        id=restaurant_id,
        is_active=True,
    ).first()
    if restaurant is None:
        raise RestrauntNotFound
    return restaurant_to_dict(restaurant)


async def update_restaurant(
    restaurant_id: int,
    payload: RestrauntResponse,
    current_user: User,
) -> dict:
    """Update an active restaurant after checking ownership."""
    restaurant = await Restraunt.filter(
        id=restaurant_id,
        is_active=True,
    ).first()
    if restaurant is None:
        raise RestrauntNotFound
    await check_restaurant_access(restaurant, current_user)
    update_data = payload.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=RESTRAUNT_EXCEPTIONS.Input_not_satisfied,
        )
    if "restaurant_name" in update_data and update_data["restaurant_name"] is None:
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
        restaurant.location_id = await get_active_address(address_id)
    for field, value in update_data.items():
        setattr(restaurant, field, value)
    restaurant.updated_by = current_user
    try:
        await restaurant.save()
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=RESTRAUNT_EXCEPTIONS.already_exists,
        ) from exc
    return restaurant_to_dict(restaurant)


async def delete_restaurant(
    restaurant_id: int,
    current_user: User,
) -> None:
    """Soft-delete an active restaurant."""
    restaurant = await Restraunt.filter(id=restaurant_id, is_active=True).first()
    if restaurant is None:
        raise RestrauntNotFound
    await check_restaurant_access(restaurant, current_user)
    restaurant.is_active = False
    restaurant.updated_by_id = current_user.id
    await restaurant.save(update_fields=["is_active", "updated_by", "updated_at"])

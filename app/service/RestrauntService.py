from tortoise.exceptions import IntegrityError
from tortoise.transactions import in_transaction

from app.exception import (
    InvalidLocationInput,
    InvalidRestaurantInput,
    RestaurantAlreadyExists,
    RestrauntNotFound,
)
from app.models import Address, Restraunt, User
from app.schemas.address import AddressCreate
from app.schemas.restraunt import RestrauntCreate, RestrauntUpdate
from app.service.AddressService import AddressService


def restaurant_to_dict(restaurant: Restraunt) -> dict:
    """Convert a restaurant model into a response-compatible dictionary.

    Arguments:
        restaurant: The active database restaurant record instance.

    Returns:
        A dictionary containing serializable restaurant data fields.
    """
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
    """Fetch an active address record by its unique identifier.

    Arguments:
        address_id: The primary key ID of the target address.

    Returns:
        The fetched active Address database model instance.

    Raises:
        RestrauntNotFound: If no active address record matches the provided ID.
    """
    try:
        address = await Address.filter(id=address_id, is_active=True).first()
    except Exception as e:
        raise e
    if address is None:
        raise RestrauntNotFound
    return address


async def check_restaurant_access(restaurant: Restraunt, current_user: User) -> None:
    """Verify that the operational session user is an administrator or restaurant owner.

    Arguments:
        restaurant: The restaurant record instance undergoing modification.
        current_user: The authenticated user session executing the request.
    """
    if current_user.is_admin:
        return


async def create_restaurant(
    payload: RestrauntCreate,
    current_user: User,
) -> dict:
    """Create a new restaurant entry and generate its corresponding address record.

    Arguments:
        payload: The Pydantic schema parameters containing new restaurant properties.
        current_user: The authenticated database user executing the operation.

    Returns:
        A dictionary containing serialized data properties of the new restaurant.

    Raises:
        RestaurantAlreadyExists: If a restaurant with the same unique name already exists.
    """
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
                location_id_id=address.id if hasattr(address, "id") else address,
                created_by_id=current_user.id,
                is_closed=payload.is_closed,
            )

    except IntegrityError as exc:
        raise RestaurantAlreadyExists() from exc
    return restaurant_to_dict(restaurant)


async def get_restaurants() -> list[dict]:
    """Return a comprehensive collection of all active restaurant records.

    Returns:
        A list of dictionaries representing active restaurants sorted by sequence ID.
    """
    restaurants = await Restraunt.filter(
        is_active=True,
    ).order_by("id")
    return [restaurant_to_dict(restaurant) for restaurant in restaurants]


async def get_restaurant(restaurant_id: int) -> dict:
    """Fetch an active restaurant record by its unique database key identifier.

    Arguments:
        restaurant_id: The primary key ID of the restaurant.

    Returns:
        A dictionary representing the target restaurant record details.

    Raises:
        RestrauntNotFound: If the restaurant record is missing or inactive.
    """
    restaurant = await Restraunt.filter(
        id=restaurant_id,
        is_active=True,
    ).first()

    if restaurant is None:
        raise RestrauntNotFound()
    return restaurant_to_dict(restaurant)


async def update_restaurant(
    restaurant_id: int,
    payload: RestrauntUpdate,
    current_user: User,
) -> dict:
    """Modify parameters of an existing active restaurant after verifying authorization.

    Arguments:
        restaurant_id: The primary key ID of the target restaurant.
        payload: The structural data schema containing modifications.
        current_user: The active session user modifying the record.

    Returns:
        A dictionary representation of the updated restaurant configuration.

    Raises:
        RestrauntNotFound: If the restaurant record is missing or inactive.
        InvalidRestaurantInput: If the payload contains no valid modification fields.
        InvalidLocationInput: If the location field update value evaluates to None.
        RestaurantAlreadyExists: If the naming changes conflict with an existing unique record.
    """
    restaurant = await Restraunt.filter(
        id=restaurant_id,
        is_active=True,
    ).first()
    if restaurant is None:
        raise RestrauntNotFound()
        
    await check_restaurant_access(restaurant, current_user)
    
    update_data = payload.model_dump(exclude_unset=True)
    if not update_data:
        raise InvalidRestaurantInput()
        
    if "location_id" in update_data:
        address_id = update_data.pop("location_id")
        if address_id is None:
            raise InvalidLocationInput()
        restaurant.location_id = await get_active_address(address_id)
        
    for field, value in update_data.items():
        setattr(restaurant, field, value)
        
    restaurant.updated_by = current_user
    try:
        await restaurant.save()
    except IntegrityError as exc:
        raise RestaurantAlreadyExists() from exc
    return restaurant_to_dict(restaurant)


async def delete_restaurant(
    restaurant_id: int,
    current_user: User,
) -> None:
    """Flag a specific restaurant record as inactive via a soft-delete transaction step.

    Arguments:
        restaurant_id: The primary key ID of the target restaurant.
        current_user: The active session user modifying the record.

    Raises:
        RestrauntNotFound: If the target restaurant does not exist or is already inactive.
    """
    restaurant = await Restraunt.filter(id=restaurant_id, is_active=True).first()
    if restaurant is None:
        raise RestrauntNotFound()
        
    await check_restaurant_access(restaurant, current_user)
    
    restaurant.is_active = False
    restaurant.updated_by_id = current_user.id
    await restaurant.save(update_fields=["is_active", "updated_by_id", "updated_at"])

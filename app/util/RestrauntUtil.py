from app.models.model import Restraunt


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

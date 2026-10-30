"""
This module provides CRUD database service actions for restaurant menu items.
"""

from fastapi import HTTPException, status
from tortoise.exceptions import IntegrityError

from app.models import Item, Restraunt, User, Owner
from app.schemas.items import ItemCreate, ItemUpdate, ItemResponse
from app.exception.AuthException import RestrauntNotFound, OwnerNotFound

async def check_restaurant_access(restaurant: Restraunt, current_user: User) -> None:
    """Verify that the user is an administrator or restaurant owner."""
    try:
        await Owner.get_or_none(user=current_user, restaurant=restaurant)
    except:
        raise OwnerNotFound()

class ItemService:
    """Provides atomic service operations for manipulating menu items."""

    @staticmethod
    async def create_item(data: ItemCreate, current_user: User) -> ItemResponse:
        """Create a new menu item bound to a restaurant after verifying owner authorization.

        Args:
            data (ItemCreate): Validated Pydantic schema parameters.
            current_user (User): The authenticated database user initiating the write step.

        Returns:
            Item: The freshly created active database Item entry.
        """
        restaurant = await Restraunt.filter(id=data.restaurant_id, is_active=True).first()
        if restaurant is None:
            raise RestrauntNotFound()

        await check_restaurant_access(restaurant, current_user)

        try:
            return await Item.create(
                item_name=data.item_name,
                restaurant=restaurant,
                created_by=current_user,
                updated_by=current_user,
                quantity=data.quantity,
                is_veg=data.is_veg,
                description=data.description,
                price=data.price,
            )
        except IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Failed to create item due to a database layout conflict.",
            ) from exc

    @staticmethod
    async def get_restaurant_menu(restaurant_id: int) -> list[ItemResponse]:
        """Fetch all active available menu items registered to a given restaurant ID.

        Args:
            restaurant_id (int): Primary key ID of the restaurant.

        Returns:
            list[Item]: Active matching items ordered sequentially by database ID.
        """
        return await Item.filter(restaurant_id=restaurant_id, is_active=True).order_by("id")

    @staticmethod
    async def get_item(item_id: int) -> ItemResponse:
        """Retrieve a specific active item configuration by its key index.

        Args:
            item_id (int): Primary key entry index.

        Returns:
            Item: The fetched active menu item.
        """
        item = await Item.filter(id=item_id, is_active=True).first()
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The requested menu item could not be found.",
            )
        return item

    @staticmethod
    async def update_item(item_id: int, data: ItemUpdate, current_user: User) -> ItemResponse:
        """Modify fields of an existing menu item record after checking restaurant access permissions.

        Args:
            item_id (int): Primary key entry index of the item.
            data (ItemUpdate): Properties to modify.
            current_user (User): The active operational session operator.

        Returns:
            Item: The updated and saved database entry configuration.
        """
        item = await Item.filter(id=item_id, is_active=True).prefetch_related("restaurant").first()
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The requested menu item could not be found.",
            )

        await check_restaurant_access(item.restaurant, current_user)

        changes = data.model_dump(exclude_unset=True)
        if not changes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No structural update parameters were supplied.",
            )

        for field, value in changes.items():
            setattr(item, field, value)

        item.updated_by = current_user
        try:
            await item.save()
        except IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Modifying item parameters triggered a database collision.",
            ) from exc
            
        return item

    @staticmethod
    async def delete_item(item_id: int, current_user: User) -> None:
        """Flag a specific menu item as inactive (soft-delete) after checking ownership access.

        Args:
            item_id (int): Primary key entry index of the target record.
            current_user (User): The active operational session operator.
        """
        item = await Item.filter(id=item_id, is_active=True).prefetch_related("restaurant").first()
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The requested menu item could not be found.",
            )

        await check_restaurant_access(item.restaurant, current_user)

        item.is_active = False
        item.updated_by = current_user
        await item.save(update_fields=["is_active", "updated_by", "updated_at"])

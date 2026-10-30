"""
This module provides service operations for owners.
"""

from tortoise.exceptions import IntegrityError

from app.exception import (
    OwnerAlreadyExistsError,
    OwnerNotFound,
    RestrauntNotFound,
    UserNotFoundError,
)
from app.models import Owner, Restraunt, User
from app.schemas import OwnerCreate, OwnerResponse


class OwnerService:
    """Provides CRUD operations for owners."""

    @staticmethod
    async def create_owner(data: OwnerCreate) -> OwnerResponse:
        """Create a new mapping record
        associating a user with a restaurant they own.

        Args:
            data (OwnerCreate): A validated Pydantic
            schema containing user_id and restraunt_id.

        Returns:
            dict: A confirmation dictionary signifying successful linkage creation.

        Raises:
            HTTPException: 404 error if either the
            target user or restaurant does not exist.
            HTTPException: 409 conflict error if this
            user-restaurant pair already exists.
        """
        try:
            user = await User.get_or_none(id=data.user_id)
            if user is None:
                raise UserNotFoundError()

            restraunt = await Restraunt.get_or_none(id=data.restraunt_id)
            if restraunt is None:
                raise RestrauntNotFound()
            return await Owner.create(user=user, restraunt=restraunt)

        except IntegrityError:
            raise OwnerAlreadyExistsError()

    @staticmethod
    async def get_all_owners() -> list[Owner]:
        """Retrieve all user-restaurant ownership
        assignments from the database sorted by ID.

        Returns:
            list[Owner]: A list containing
            all Owner association records.
        """
        return await Owner.all().select_related("user", "restraunt")

    @staticmethod
    async def get_owner(owner_id: int) -> Owner:
        """Retrieve a specific ownership
        association record by its database ID.

        Args:
            owner_id (int): The unique integer
            database ID of the ownership entry.

        Returns:
            Owner: The matching retrieved Owner database instance.

        Raises:
            HTTPException: 404 error if no ownership
            relationship matches the provided ID.
        """
        owner = await Owner.get_or_none(id=owner_id)
        if owner is None:
            raise OwnerNotFound()
        return owner

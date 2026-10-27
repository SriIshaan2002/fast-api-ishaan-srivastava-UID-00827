"""
This module provides CRUD operations for owners.
"""
from fastapi import APIRouter, HTTPException, status
from tortoise.exceptions import IntegrityError

from app.models import Owner
from app.schemas import OwnerCreate, OwnerUpdate, OwnerResponse

from constants import OWNER_ERRORS

router = APIRouter(prefix="/owners", tags=["Owners"])

@router.post(
    "/",
    response_model=OwnerResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_owner(data: OwnerCreate):
    """Create a new owner."""
    try:
        owner = await Owner.create(
            username=data.username,
            email=str(data.email).lower(),
            mobile=data.mobile,
            password=data.password,
        )
        return owner
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=OWNER_ERRORS.already_exists,
        ) from exc

@router.get("/", response_model=list[OwnerResponse])
async def get_all_owners():
    """Retrieve all owners."""
    return await Owner.all().order_by("id")

@router.get("/{owner_id}", response_model=OwnerResponse)
async def get_owner(owner_id: int):
    """Retrieve an owner by ID."""
    owner = await Owner.get_or_none(id=owner_id)
    if owner is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=OWNER_ERRORS.not_found,
        )
    return owner

@router.patch("/{owner_id}", response_model=OwnerResponse)
async def update_owner(owner_id: int, data: OwnerUpdate):
    """Update an owner's permitted fields."""
    owner = await Owner.get_or_none(id=owner_id)
    if owner is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=OWNER_ERRORS.not_found,
        )
    changes = data.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(owner, field, value)
    if changes:
        try:
            await owner.save()
        except IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=OWNER_ERRORS.already_exists,
            ) from exc
    return owner

@router.delete("/{owner_id}",status_code=status.HTTP_204_NO_CONTENT,)
async def delete_owner(owner_id: int):
    """Delete an owner."""
    owner = await Owner.get_or_none(id=owner_id)
    if owner is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=OWNER_ERRORS.not_found,
        )
    await owner.delete()
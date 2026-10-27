from decimal import Decimal
from uuid import UUID

from tortoise import fields, models

from enums import OrderStatus
from enums import Tables as tab


class BaseModel(models.Model):
    """Provide a primary key for database models."""

    id: int = fields.IntField(primary_key=True)

    class Meta:
        abstract = True


class TimestampModel(BaseModel):
    """Provide creation and modification timestamps."""

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class ActiveModel(TimestampModel):
    """Provide timestamps and an active-status flag."""

    is_active: bool = fields.BooleanField(default=True)

    class Meta:
        abstract = True


class AuditModel(ActiveModel):
    """Provide active status, timestamps, and modifier tracking."""

    updated_by: fields.ForeignKeyNullableRelation["User"] = fields.ForeignKeyField(
        "models.User",
        null=True,
        on_delete=fields.SET_NULL,
    )

    class Meta:
        abstract = True


class User(ActiveModel):
    """Represent a user account with profile, balance, and account status."""

    username: str = fields.CharField(max_length=20)
    mobile: str = fields.CharField(max_length=13, null=True)
    email: str = fields.CharField(max_length=254, unique=True)
    password: str = fields.CharField(max_length=255)
    balance: "Decimal" = fields.DecimalField(max_digits=10, decimal_places=3, default=0)
    is_admin: bool = fields.BooleanField(default=False)
    updated_by: fields.ForeignKeyNullableRelation["User"] = fields.ForeignKeyField(
        "models.User",
        related_name="user_self_updates",
        null=True,
        on_delete=fields.SET_NULL,
    )

    class Meta:
        table = tab.USER.value


class Token(BaseModel):
    """Store refresh-token records associated with user accounts."""

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User",
        related_name="tokens",
        on_delete=fields.CASCADE,
    )
    uuid: UUID = fields.UUIDField(unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    exp_at = fields.DateTimeField()
    revoked_at = fields.DatetimeField(null=True)

    class Meta:
        table = tab.TOKEN.value


class Address(AuditModel):
    """Represent a user's address, including geographic coordinates."""

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User",
        related_name="addresses",
        on_delete=fields.RESTRICT,
    )
    city: str = fields.CharField(max_length=50)
    street: str = fields.CharField(max_length=100)
    house: str = fields.CharField(max_length=50)
    zip: str = fields.CharField(max_length=10)
    nearby_location: str | None = fields.CharField(max_length=100, null=True)
    long: Decimal | None = fields.DecimalField(
        max_digits=11, decimal_places=8, null=True
    )
    lat: Decimal | None = fields.DecimalField(
        max_digits=10, decimal_places=8, null=True
    )

    class Meta:
        table = tab.ADDRESS.value


class Restraunt(AuditModel):
    """Store restaurant operational records."""

    restaurant_name: str = fields.CharField(max_length=50, unique=True)
    location_id: fields.ForeignKeyRelation[Address] = fields.ForeignKeyField(
        "models.Address",
        related_name="restaurants",
        on_delete=fields.RESTRICT,
    )
    created_by: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User",
        related_name="created_restaurants",
        on_delete=fields.RESTRICT,
    )
    is_closed: bool = fields.BooleanField(default=True)

    class Meta:
        table = tab.RESTRAUNT.value


class Item(AuditModel):
    """Represent a menu item offered by a restaurant."""

    item_name: str = fields.CharField(max_length=50)
    restaurant: fields.ForeignKeyRelation[Restraunt] = fields.ForeignKeyField(
        "models.Restraunt",
        related_name="items",
        on_delete=fields.RESTRICT,
    )
    created_by: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User",
        related_name="created_items",
        on_delete=fields.RESTRICT,
    )
    quantity: int = fields.IntField(default=0)
    is_veg: bool = fields.BooleanField()
    description: str | None = fields.CharField(max_length=500, null=True)
    price: Decimal = fields.DecimalField(max_digits=10, decimal_places=3)
    class Meta:
        table = tab.ITEM.value


class Order(AuditModel):
    """Represent a customer's order and its delivery information."""

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User",
        related_name="user_orders",
        on_delete=fields.RESTRICT,
    )
    restaurant: fields.ForeignKeyRelation[Restraunt] = fields.ForeignKeyField(
        "models.Restraunt",
        related_name="restraunt_orders",
        on_delete=fields.RESTRICT,
    )
    delivery_location: fields.ForeignKeyNullableRelation[Address] = (
        fields.ForeignKeyField(
            "models.Address",
            related_name="delivered_orders",
            null=True,
            on_delete=fields.SET_NULL,
        )
    )
    total_price: "Decimal" = fields.DecimalField(max_digits=10, decimal_places=3)
    status: OrderStatus = fields.CharEnumField(
        OrderStatus,
        max_length=20,
        default=OrderStatus.PENDING,
    )

    class Meta:
        table = tab.ORDER.value


class OrderItem(BaseModel):
    """Represent an individual item snapshot associated with an order."""

    order: fields.ForeignKeyRelation[Order] = fields.ForeignKeyField(
        "models.Order",
        related_name="order_items",
        on_delete=fields.CASCADE,
    )
    item_name: str = fields.CharField(max_length=50)
    is_veg: bool = fields.BooleanField(default=True)
    quantity: int = fields.IntField()
    discount: int = fields.IntField(default=0)
    price: Decimal = fields.DecimalField(max_digits=10, decimal_places=3)
    is_active: bool = fields.BooleanField(default=True)

    class Meta:
        table = tab.ORDER_ITEM.value


class Owner(AuditModel):
    """Associate a user with restaurants they own."""

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User",
        related_name="ownerships",
        on_delete=fields.CASCADE,
    )
    restraunt: fields.ForeignKeyRelation[Restraunt] = fields.ForeignKeyField(
        "models.Restraunt",
        related_name="owners",
        on_delete=fields.CASCADE,
    )

    class Meta:
        table = tab.OWNER.value
        unique_together = (("user", "restraunt"),)

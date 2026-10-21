from enum import Enum
from tortoise import fields, models

class OrderStatus(str, Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    PREPARING = "Preparing"
    ON_THE_WAY = "On-the-Way"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"
    RETURNED = "Returned"


class User(models.Model):
    id = fields.IntField(primary_key=True)

    username = fields.CharField(max_length=20)
    mobile = fields.CharField(max_length=13, unique=True)
    email = fields.CharField(max_length=254, unique=True)

    balance = fields.DecimalField(
        max_digits=10, decimal_places=3, default=0
    )
    is_admin = fields.BooleanField(default=False)
    is_active = fields.BooleanField(default=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(null=True)

    updated_by = fields.ForeignKeyField(
        "models.User",
        related_name="updated_users",
        null=True,
        on_delete=fields.SET_NULL,
    )

    class Meta:
        table = "users"


class Token(models.Model):
    id = fields.IntField(primary_key=True)

    user = fields.ForeignKeyField(
        "models.User",
        related_name="tokens",
        on_delete=fields.CASCADE,
    )
    refresh = fields.UUIDField(unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    revoked_at = fields.DatetimeField(null=True)
    class Meta:
        table = "token"


class Restraunt(models.Model):
    id = fields.IntField(primary_key=True)

    restaurant_name = fields.CharField(max_length=20, unique=True)
    state = fields.CharField(max_length=15)
    city = fields.CharField(max_length=15)
    zip = fields.CharField(max_length=10)
    street = fields.CharField(max_length=50)
    nearby_location = fields.CharField(max_length=50, null=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(null=True)

    created_by = fields.ForeignKeyField(
        "models.User",
        related_name="created_restaurants",
        on_delete=fields.RESTRICT,
    )

    updated_by = fields.ForeignKeyField(
        "models.User",
        related_name="updated_restaurants",
        null=True,
        on_delete=fields.SET_NULL,
    )

    is_closed = fields.BooleanField(default=True)
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "restraunts"


class Address(models.Model):
    id = fields.IntField(primary_key=True)

    user = fields.ForeignKeyField(
        "models.User",
        related_name="addresses",
        on_delete=fields.RESTRICT,
    )

    created_at = fields.DatetimeField(auto_now_add=True)

    city = fields.CharField(max_length=50)
    street = fields.CharField(max_length=50)
    house = fields.CharField(max_length=20)
    zip = fields.CharField(max_length=10)
    nearby_location = fields.CharField(max_length=50, null=True)

    long = fields.DecimalField(
        max_digits=11, decimal_places=8, null=True
    )
    lat = fields.DecimalField(
        max_digits=10, decimal_places=8, null=True
    )

    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "address"


class Item(models.Model):
    id = fields.IntField(primary_key=True)

    item_name = fields.CharField(max_length=20)

    restaurant = fields.ForeignKeyField(
        "models.Restraunt",
        related_name="items",
        on_delete=fields.RESTRICT,
    )

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(null=True)

    created_by = fields.ForeignKeyField(
        "models.User",
        related_name="created_items",
        on_delete=fields.RESTRICT,
    )

    updated_by = fields.ForeignKeyField(
        "models.User",
        related_name="updated_items",
        null=True,
        on_delete=fields.SET_NULL,
    )

    quantity = fields.IntField(default=0)
    is_veg = fields.BooleanField()
    description = fields.CharField(max_length=255, null=True)

    price = fields.DecimalField(
        max_digits=10, decimal_places=3
    )

    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "items"


class Order(models.Model):
    id = fields.IntField(primary_key=True)

    user = fields.ForeignKeyField(
        "models.User",
        related_name="orders",
        on_delete=fields.RESTRICT,
    )

    restaurant = fields.ForeignKeyField(
        "models.Restraunt",
        related_name="orders",
        on_delete=fields.RESTRICT,
    )

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(null=True)

    created_by = fields.ForeignKeyField(
        "models.User",
        related_name="created_orders",
        null=True,
        on_delete=fields.SET_NULL,
    )

    updated_by = fields.ForeignKeyField(
        "models.User",
        related_name="updated_orders",
        null=True,
        on_delete=fields.SET_NULL,
    )

    delivery_location = fields.ForeignKeyField(
        "models.Address",
        related_name="orders",
        null=True,
        on_delete=fields.SET_NULL,
    )

    delivered_in = fields.DatetimeField(null=True)

    total_price = fields.DecimalField(
        max_digits=10, decimal_places=3
    )

    status = fields.CharEnumField(
        OrderStatus,
        max_length=20,
        default=OrderStatus.PENDING,
    )

    delivered_by = fields.ForeignKeyField(
        "models.User",
        related_name="delivered_orders",
        null=True,
        on_delete=fields.SET_NULL,
    )

    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "orders"


class OrderItem(models.Model):
    id = fields.IntField(primary_key=True)

    order = fields.ForeignKeyField(
        "models.Order",
        related_name="order_items",
        on_delete=fields.CASCADE,
    )

    item_name = fields.CharField(max_length=20)
    is_veg = fields.BooleanField(default=True)

    quantity = fields.IntField()
    discount = fields.IntField(default=0)

    price = fields.DecimalField(
        max_digits=10, decimal_places=3
    )

    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "order_items"


class Owner(models.Model):
    id = fields.IntField(primary_key=True)

    user = fields.ForeignKeyField(
        "models.User",
        related_name="ownerships",
        on_delete=fields.CASCADE,
    )

    restraunt = fields.ForeignKeyField(
        "models.Restraunt",
        related_name="owners",
        on_delete=fields.CASCADE,
    )

    class Meta:
        table = "owners"
        unique_together = (("user", "restraunt"),)
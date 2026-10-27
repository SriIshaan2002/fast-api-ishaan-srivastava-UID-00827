"""Define database models and order statuses for the restaurant management system."""

from enums import OrderStatus, Tables as tab
from tortoise import fields, models

class BaseModel(models.Model):
    """Provide a primary key for database models."""
    id = fields.IntField(primary_key=True)
    class Meta:
        abstract = True

class TimestampModel(BaseModel):
    """Provide creation and modification timestamps."""
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(null=True)
    class Meta:
        abstract = True

class ActiveModel(TimestampModel):
    """Provide timestamps and an active-status flag."""
    is_active = fields.BooleanField(default=True)
    class Meta:
        abstract = True

class AuditModel(ActiveModel):
    """Provide active status, timestamps, and modifier tracking."""
    updated_by = fields.ForeignKeyField(
        "models.User",
        null=True,
        on_delete=fields.SET_NULL,
    )
    class Meta:
        abstract = True

class User(ActiveModel):
    """Represent a user account with profile, balance, and account status."""
    username = fields.CharField(max_length=20)
    mobile = fields.CharField(max_length=13, unique=True)
    email = fields.CharField(max_length=254, unique=True)
    password = fields.CharField(max_length=255)
    balance = fields.DecimalField(max_digits=10, decimal_places=3, default=0)
    is_admin = fields.BooleanField(default=False)
    updated_by = fields.ForeignKeyField(
        "models.User",
        related_name="user_self_updates",
        null=True,
        on_delete=fields.SET_NULL,
    )
    class Meta:
        table = tab.USER.value

class Token(BaseModel):
    """Store refresh-token records associated with user accounts."""
    user = fields.ForeignKeyField(
        "models.User",
        related_name="tokens",
        on_delete=fields.CASCADE,
    )
    uuid = fields.UUIDField(unique=True)
    token = fields.CharField(max_length=500)
    created_at = fields.DatetimeField(auto_now_add=True)
    revoked_at = fields.DatetimeField(null=True)
    class Meta:
        table = tab.TOKEN.value

class Address(AuditModel):
    """Represent a user's address, including geographic coordinates."""
    user = fields.ForeignKeyField(
        "models.User",
        related_name="addresses",
        on_delete=fields.RESTRICT,
    )
    city = fields.CharField(max_length=50)
    street = fields.CharField(max_length=100)
    house = fields.CharField(max_length=50)
    zip = fields.CharField(max_length=10)
    nearby_location = fields.CharField(max_length=100, null=True)
    long = fields.DecimalField(max_digits=11, decimal_places=8, null=True)
    lat = fields.DecimalField(max_digits=10, decimal_places=8, null=True)
    class Meta:
        table = tab.ADDRESS.value

class Restraunt(AuditModel):
    """Store restaurant operational records."""
    restaurant_name = fields.CharField(max_length=50, unique=True)
    location_id = fields.ForeignKeyField(
        "models.Address",
        related_name="restaurants",
        on_delete=fields.RESTRICT,
    )
    created_by = fields.ForeignKeyField(
        "models.User",
        related_name="created_restaurants",
        on_delete=fields.RESTRICT,
    )
    is_closed = fields.BooleanField(default=True)
    class Meta:
        table = tab.RESTRAUNT.value

class Item(AuditModel):
    """Represent a menu item offered by a restaurant."""
    item_name = fields.CharField(max_length=50)
    restaurant = fields.ForeignKeyField(
        "models.Restraunt",
        related_name="items",
        on_delete=fields.RESTRICT,
    )
    created_by = fields.ForeignKeyField(
        "models.User",
        related_name="created_items",
        on_delete=fields.RESTRICT,
    )
    quantity = fields.IntField(default=0)
    is_veg = fields.BooleanField()
    description = fields.CharField(max_length=500, null=True)
    price = fields.DecimalField(max_digits=10, decimal_places=3)
    class Meta:
        table = tab.ITEM.value

class Order(AuditModel):
    """Represent a customer's order and its delivery information."""
    user = fields.ForeignKeyField(
        "models.User",
        related_name="user_orders",
        on_delete=fields.RESTRICT,
    )
    restaurant = fields.ForeignKeyField(
        "models.Restraunt",
        related_name="restraunt_orders",
        on_delete=fields.RESTRICT,
    )
    created_by = fields.ForeignKeyField(
        "models.User",
        related_name="created_orders",
        null=True,
        on_delete=fields.SET_NULL,
    )
    delivery_location = fields.ForeignKeyField(
        "models.Address",
        related_name="delivered_orders",
        null=True,
        on_delete=fields.SET_NULL,
    )
    total_price = fields.DecimalField(max_digits=10, decimal_places=3)
    status = fields.CharEnumField(
        OrderStatus,
        max_length=20,
        default=OrderStatus.PENDING,
    )
    class Meta:
        table = tab.ORDER.value

class OrderItem(BaseModel):
    """Represent an individual item snapshot associated with an order."""
    order = fields.ForeignKeyField(
        "models.Order",
        related_name="order_items",
        on_delete=fields.CASCADE,
    )
    item_name = fields.CharField(max_length=50)
    is_veg = fields.BooleanField(default=True)
    quantity = fields.IntField()
    discount = fields.IntField(default=0)
    price = fields.DecimalField(max_digits=10, decimal_places=3)
    is_active = fields.BooleanField(default=True)
    class Meta:
        table = tab.ORDER_ITEM.value

class Owner(BaseModel):
    """Associate a user with restaurants they own."""
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
        table = tab.OWNER.value
        unique_together = (("user", "restraunt"),)
        
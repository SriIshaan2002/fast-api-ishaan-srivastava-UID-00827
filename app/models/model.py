"""Define database models and order statuses for the restaurant management system."""
from enum import Enum
from tortoise import fields, models
from tables import Tables as tab

class OrderStatus(str, Enum):
    """Represent the possible statuses of a restaurant order."""
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    PREPARING = "Preparing"
    ON_THE_WAY = "On-the-Way"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"
    RETURNED = "Returned"

class User(models.Model):
    """Represent a user account with profile, balance, and account status."""
    id = fields.IntField(primary_key=True)
    username = fields.CharField(max_length=20)
    mobile = fields.CharField(max_length=13, unique=True)
    email = fields.CharField(max_length=254, unique=True)
    password = fields.CharField(max_length=255)
    balance = fields.DecimalField(max_digits=10, decimal_places=3, default=0)
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
        """Configure the database table for user records."""
        table = tab.USERS.value

class Token(models.Model):
    """Store refresh-token records associated with user accounts."""
    user = fields.ForeignKeyField(
        "models.User",
        related_name="tokens",
        on_delete=fields.CASCADE,
    )
    uuid = fields.UUIDField(unique=True)
    token = fields.CharField(max_length=500) 
    created_at = fields.DatetimeField(auto_now_add=True)
    class Meta:
        table = tab.TOKENS.value

class Restraunt(models.Model):
    """Store refresh-token records associated with user accounts."""
    id = fields.IntField(primary_key=True)
    restaurant_name = fields.CharField(max_length=20, unique=True)
    location_id = fields.ForeignKeyField(
        "models.Address",
        related_name="restaurants",
        on_delete=fields.RESTRICT,
    )
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
        """Configure the database table for restaurant records."""
        table = tab.RESTRAUNTS.value

class Address(models.Model):
    """Represent a user's address, including geographic coordinates."""
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
    long = fields.DecimalField(max_digits=11, decimal_places=8, null=True)
    lat = fields.DecimalField(max_digits=10, decimal_places=8, null=True)
    is_active = fields.BooleanField(default=True)
    class Meta:
        """Configure the database table for address records."""
        table = tab.ADDRESS.value

class Item(models.Model):
    """Represent a menu item offered by a restaurant."""
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
        """Configure the database table for menu items."""
        table = tab.ITEMS.value

class Order(models.Model):
    """Represent a customer's order and its delivery information."""
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
        """Configure the database table for orders."""
        table = tab.ORDERS.value

class OrderItem(models.Model):
    """Represent an individual item snapshot associated with an order."""
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
        """Configure the database table for order items."""
        table = tab.ORDER_ITEMS.value

class Owner(models.Model):
    """Associate users with restaurants they own."""
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
        table = tab.OWNERS.value
        unique_together = (("user", "restraunt"),)

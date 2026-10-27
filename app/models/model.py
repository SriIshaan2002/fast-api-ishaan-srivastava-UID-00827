"""Define database models and order statuses for the restaurant management system."""

from enums import Tables as tab, OrderStatus

from tortoise import fields, models


class BaseAuditModel(models.Model):
    """Abstract interface enforcing tracking parameters on subordinate tables."""

    id = fields.IntField(primary_key=True)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(null=True)

    class Meta:
        abstract = True


class AuditModel(BaseAuditModel):
    """Extended abstract interface incorporating modifier tracking capabilities."""

    updated_by = fields.ForeignKeyField(
        "models.User",
        null=True,
        on_delete=fields.SET_NULL,
    )

    class Meta:
        abstract = True


class User(BaseAuditModel):
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
        """Configure the database table for user records."""

        table = tab.USER.value


class Token(models.Model):
    """Store refresh-token records associated with user accounts."""

    id = fields.IntField(primary_key=True)
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
        """Configure the database table for address records."""

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
        """Configure the database table for restaurant records."""

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
        """Configure the database table for menu Item."""

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
        """Configure the database table for Order."""

        table = tab.ORDER.value


class OrderItem(models.Model):
    """Represent an individual item snapshot associated with an order."""

    id = fields.IntField(primary_key=True)
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
        """Configure the database table for order Item."""

        table = tab.ORDER_ITEM.value


class Owner(models.Model):
    """Associate User with restaurants they own."""

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
        table = tab.OWNER.value
        unique_together = (("user", "restraunt"),)

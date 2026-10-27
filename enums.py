from enum import Enum

class Tables(str, Enum):
    ADDRESS = "address"
    ITEM = "item"
    ORDER_ITEM = "order_item"
    ORDER = "order"
    OWNER = "owner"
    RESTRAUNT = "restraunt"
    TOKEN = "token"
    USER = "user"

class OrderStatus(str, Enum):
    """Represent the possible statuses of a restaurant order."""
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    PREPARING = "Preparing"
    ON_THE_WAY = "On-the-Way"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"
    RETURNED = "Returned"
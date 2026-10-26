from enum import Enum


class Tables(str, Enum):
    ADDRESS = "addresses"
    ITEMS = "items"
    ORDER_ITEMS = "order_items"
    ORDERS = "orders"
    OWNERS = "owners"
    RESTRAUNTS = "restraunts"
    TOKENS = "tokens"
    USERS = "users"

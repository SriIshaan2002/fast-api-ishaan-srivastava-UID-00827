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

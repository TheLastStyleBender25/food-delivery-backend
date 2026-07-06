from enum import Enum

class RestaurantStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    TEMPORARILY_CLOSED = "TEMPORARILY_CLOSED"
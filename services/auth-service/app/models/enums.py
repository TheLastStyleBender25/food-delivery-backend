from enum import Enum

class UserRole(str, Enum):
    CUSTOMER = "CUSTOMER"
    RESTAURANT_OWNER = "RESTAURANT_OWNER"
    DRIVER = "DRIVER"
    ADMIN = "ADMIN"
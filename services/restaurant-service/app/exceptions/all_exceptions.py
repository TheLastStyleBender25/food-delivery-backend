class RestaurantNotFound(Exception):
    pass

class InvalidRestaurant(Exception):
    pass

class NonRestaurantOwner(Exception):
    pass

class NonCustomerException(Exception):
    pass

class RestaurantNotOpenException(Exception):
    pass

class RateLimitExceededException(Exception):
    pass

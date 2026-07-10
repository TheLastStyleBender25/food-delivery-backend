class RestaurantNotFound(Exception):
    pass

class InvalidRestaurant(Exception):
    pass

class NonRestaurantOwner(Exception):
    pass

class NonCustomerException(Exception):
    pass

class RateLimitExceededException(Exception):
    pass

class MenuItemNotFoundException(Exception):
    pass

class ForbiddenException(Exception):
    pass

class RestaurantServiceUnavailableException(Exception):
    pass

class RequestTimeoutException(Exception):
    pass

class InvalidImageExtensionException(Exception):
    pass

class InvalidImageTypeException(Exception):
    pass

class InvalidImageContentException(Exception):
    pass

class FileTooLargeException(Exception):
    pass


class RateLimitExceededException(Exception):
    pass

class CartNotFoundException(Exception):
    pass

class ForbiddenException(Exception):
    pass

class CartServiceUnavailableException(Exception):
    pass

class RequestTimeoutException(Exception):
    pass


class CartItemNotFoundException(Exception):
    pass

class MenuItemNotFoundException(Exception):
    pass

class MenuServiceUnavailableException(Exception):
    pass

class OrderNotFoundException(Exception):
    pass

class CannotCancelOrderException(Exception):
    pass


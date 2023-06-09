
class UnauthorizedException(Exception):
    """
    Raised when the API returns an unauthorized status code
    """
    pass

class InternalServerErrorException(Exception):
    """
    Raised when the API returns an internal server error.
    """
    pass


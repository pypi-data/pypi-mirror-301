class LunarDBException(Exception):
    """Base exception for LunarDB SDK"""
    pass

class ConnectionError(LunarDBException):
    """Raised when there's an issue connecting to the LunarDB server"""
    pass

class AuthenticationError(LunarDBException):
    """Raised when there's an authentication problem"""
    pass

class KeyError(LunarDBException):
    """Raised when there's an issue with a key operation"""
    pass

class ServerError(LunarDBException):
    """Raised when the server returns an unexpected error"""
    pass

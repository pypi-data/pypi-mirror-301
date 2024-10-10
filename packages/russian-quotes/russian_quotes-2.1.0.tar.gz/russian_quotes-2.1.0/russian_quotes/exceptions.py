class ServerError(Exception):
    """
    Custom exception for server errors.

    This error is raised when the server status is not 200.
    """
    pass

class LanguageIsNotSupported(Exception):
    """
    Custom exception for language errors.

    This error is raised when language is not supported.
    """
    pass
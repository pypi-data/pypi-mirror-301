class InternalServerError(Exception):
    """Raised when the API returns a 5xx status code"""
    def __init__(self, message):
        self.message = message

class ClientError(Exception):
    """Raised when the API returns a 4xx status code"""
    def __init__(self, message):
        self.message = message

class TooManyRequests(Exception):
    """Raised when the API returns a 429 status code"""
    def __init__(self, message):
        self.message = message

class RetryLimitExceeded(Exception):
    """Raised when the retry limit is exceeded"""
    def __init__(self, message):
        self.message = message

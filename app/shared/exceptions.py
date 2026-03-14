class NotFoundError(Exception):
    def __init__(self, resource: str = ''):
        self.resource = resource


class UnauthorizedError(Exception):
    def __init__(self, message: str = 'Unauthorized'):
        self.message = message


class ConflictError(Exception):
    def __init__(self, message: str = 'Action cannot be completed'):
        self.message = message


class UnprocessableError(Exception):
    def __init__(self, message: str = ''):
        self.message = message


class InvalidCredentialsError(Exception):
    def __init__(self, message: str = 'Invalid credentials'):
        self.message = message


class QuotaExceededError(Exception):
    def __init__(self, message: str = 'Invalid credentials'):
        self.message = message

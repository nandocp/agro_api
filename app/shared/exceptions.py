class AgroAPIError(Exception):
    def __init__(self, code: str, message: str = ''):
        self.code = code
        self.message = message


class NotFoundError(AgroAPIError):
    def __init__(self, resource: str):
        super().__init__(code=f'not_found.{resource}')


class UnauthorizedError(AgroAPIError):
    def __init__(self):
        super().__init__(code='auth.unauthorized')


class ForbiddenError(AgroAPIError):
    def __init__(self):
        super().__init__(code='auth.forbidden')


class InvalidCredentialsError(AgroAPIError):
    def __init__(self):
        super().__init__(code='auth.invalid_credentials')


class ConflictError(AgroAPIError):
    def __init__(self, resource: str = ''):
        super().__init__(
            code=f'conflict.{resource}' if resource else 'conflict.generic'
        )


class UnprocessableError(AgroAPIError):
    def __init__(self, resource: str = ''):
        super().__init__(
            code=f'unprocessable.{resource}'
            if resource
            else 'unprocessable.generic'
        )


class QuotaExceededError(AgroAPIError):
    def __init__(self, resource: str):
        super().__init__(code=f'quota.{resource}_limit_reached')

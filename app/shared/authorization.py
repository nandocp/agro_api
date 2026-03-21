from functools import wraps

from app.domain.accounts.models import User
from app.shared.enums import Action, Resource
from app.shared.exceptions import UnauthorizedError


class AuthorizationService:
    @staticmethod
    def has_permission(user: User, resource: Resource, action: Action) -> bool:
        if user.deactivated_at:
            return False

        # Alhtough this has a O(n x p) complexity, the system has a small
        # set of possibilities of roles and permissions.
        # The performance gain is not problematic in here.
        permissions = {
            (p.resource, p.action)
            for role in user.roles
            for p in role.permissions
        }

        return (resource.value, action.value) in permissions

    def check(user: User, resource: Resource, action: Action) -> None:
        if not AuthorizationService.has_permission(user, resource, action):
            raise UnauthorizedError


@staticmethod
def require_permission(resource: Resource, action: Action):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            current_user = kwargs.get('current_user')

            # fallback
            if current_user is None:
                current_user = next(
                    (a for a in args if isinstance(a, User)), None
                )

            if current_user is None:
                raise UnauthorizedError()

            AuthorizationService.check(current_user, resource, action)

            return await func(self, *args, **kwargs)

        return wrapper

    return decorator

from functools import wraps

from app.domain.accounts.models import User
from app.shared.enums import Action, Resource
from app.shared.exceptions import UnauthorizedError


@staticmethod
class AuthorizationService:
    def has_permission(user: User, resource: Resource, action: Action) -> bool:
        if user.deactivated_at:
            return False

        permissions = {
            (p.resource, p.action)
            for role in user.roles
            for p in role.permissions
        }

        if (resource.value, Action.MANAGE.value) in permissions:
            return True

        return (resource.value, action.value) in permissions

    def check(self, user: User, resource: Resource, action: Action) -> None:
        if not self.has_permission(user, resource, action):
            raise UnauthorizedError


def require_permission(resource: Resource, action: Action):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            current_user = kwargs.get('current_user')
            if current_user is None:
                # fallback — busca nos args pela tipagem
                current_user = next(
                    (a for a in args if isinstance(a, User)), None
                )
            if current_user is None:
                raise UnauthorizedError()

            AuthorizationService.check(current_user, resource, action)
            return await func(self, *args, **kwargs)

        return wrapper

    return decorator

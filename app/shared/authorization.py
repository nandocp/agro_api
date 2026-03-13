from app.domain.accounts.models import User
from app.shared.enums import Action, Resource
from app.shared.exceptions import UnauthorizedError


@staticmethod
class AuthorizationService:
    def has_permission(user: User, resource: Resource, action: Action) -> bool:
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

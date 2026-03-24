from fastapi import APIRouter, Depends

from app.shared.dependencies import CurrentUser
from app.shared.exceptions import ForbiddenError

from .accounts import router as account_router
from .users import router as users_router


async def require_superuser(current_user: CurrentUser) -> None:
    is_superuser = any(role.name == 'superuser' for role in current_user.roles)
    if not is_superuser:
        raise ForbiddenError


router = APIRouter(
    dependencies=[
        Depends(require_superuser),
    ]
)

router.include_router(account_router, prefix='/accounts')
router.include_router(users_router, prefix='/users')

from agro_api.entities.core import User
from agro_api.schemas.user import UserCreate, UserUpdate
from agro_api.services.core import UserService
from config.authentication import current_user
from config.database import session


async def create_user(params: UserCreate, session: session):
    service = UserService(session=session, model=User)
    return await service.create(params)


async def get_user(user: current_user, user_id: str, session: session):
    service = UserService(session=session, model=User, current_user=user)

    # TO-DO: only Admin User will be able to get another User
    return await service.get_one(user_id)


async def update_user(
    params: UserUpdate, session: session, user: current_user, user_id: str
):
    service = UserService(session=session, model=User, current_user=user)

    return await service.update(params=params, user_id=user_id)

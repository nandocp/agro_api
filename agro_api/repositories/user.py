from agro_api.entities.user import User
from agro_api.repositories.base import BaseRepository
from agro_api.schemas.user import UserBase, UserCreate


class UserRepository(BaseRepository[User, UserBase, UserCreate]):
    pass

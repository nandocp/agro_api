from agro_api.entities.user import User
from agro_api.repositories.user import UserRepository
from config.password import hash_password

from .base import BaseService


class UserService(BaseService):
    def __init__(self, session=None):
        super().__init__(User)
        self.repository = UserRepository(session)

    def create(self, schema_params):
        schema_params.password = hash_password(schema_params.password)
        return self.repository.create_user(schema_params)

    def get_one(self, id: str, jti: str):
        user = self.repository.find_by_jti(jti)

        if not user or str(user.id) != id:
            return False

        return user

    def get_many(self, *, skip: int = 0, limit: int = 100):
        pass

    def update(self, obj_id, obj_in):
        return self.repository.update_user(obj_id, obj_in)

    def remove(self, *, id: int):
        pass

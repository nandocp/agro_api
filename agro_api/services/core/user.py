from agro_api.services.base import BaseService
from config.authentication import validate_current_user
from config.http_misc import unauthorized, with_conflict
from config.password import hash_password


class UserService(BaseService):
    async def create(self, schema_params):
        db_user = await self.repository.get_by({'email': schema_params.email})

        if db_user:
            with_conflict('User already exists')

        schema_params.password = hash_password(schema_params.password)

        return await self.repository.create(obj_in=schema_params)

    async def get_one(self, user_id: str):
        validate_current_user(user_id, str(self.user.id))
        # eventualmente implementar caso de admin user

        return self.user

    async def update(self, *, user_id: str, params):
        validate_current_user(user_id, str(self.user.id))

        user = await self.repository.get_one(user_id)

        if not user:
            unauthorized()

        update_params = {'name': params.name}

        await self.repository.update(db_obj=user, obj_in=update_params)

        return user

from agro_api.entities.estate import Estate

from .base import BaseService


class EstateService(BaseService):
    def __init__(self, session=None):
        super().__init__(Estate, session)

    def create(self, schema_params, user_id):
        new_estate = self.model(
            **schema_params.model_dump(),
            user_id=user_id
        )

        self.session.add(new_estate)
        self.session.commit()
        self.session.refresh(new_estate)

        return new_estate

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

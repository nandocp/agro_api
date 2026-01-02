from sqlalchemy import select

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

    def get_one(self, user_id: str, e_id: str):
        return self.session.scalar(
            select(Estate).where(
                Estate.id == e_id and Estate.user_id == user_id
            )
        )

    def get_many(self, user_id, filters):
        query = select(Estate).where(Estate.user_id == user_id)

        if filters.kind:
            query = query.filter(Estate.kind == filters.kind)

        if filters.label:
            query = query.filter(Estate.label.contains(filters.label))

        if filters.slug:
            query = query.filter(Estate.slug == filters.slug)

        return {'estates': self.session.scalars(query).all()}

    def update(self, obj_id, obj_in):
        print(self)
        return obj_in

    def remove(self, *, id: int):
        pass

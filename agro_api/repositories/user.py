from http import HTTPStatus

from sqlalchemy import select
from sqlalchemy.orm import Session

from agro_api.entities.user import User


class UserRepository:
    def __init__(self, session=None):
        self.session: Session | None = session

    def create_user(self, schema_params) -> User:
        db_user = self.session.scalar(
            select(User).where(User.email == schema_params.email)
        )

        if db_user:
            return {
                'status_code': HTTPStatus.CONFLICT,
                'detail': 'User already exists',
            }

        new_user = User(**schema_params.model_dump())

        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)

        return new_user

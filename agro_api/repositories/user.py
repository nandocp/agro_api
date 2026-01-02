from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from agro_api.entities.user import User
from config.password import verify_password


class UserRepository:
    def __init__(self, session=None):
        self.session: Session | None = session

    def find_by_email(self, email) -> User:
        return self.session.scalar(select(User).where(User.email == email))

    def find_by_jti(self, jti) -> User | None:
        return self.session.scalar(select(User).where(User.jti == jti))

    def create_user(self, schema_params) -> User:
        db_user = self.find_by_email(schema_params.email)

        if db_user:
            return False

        new_user = User(**schema_params.model_dump())

        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)

        return new_user

    def update_user(self, user_id, new_params):
        db_user = self.session.scalar(select(User).where(User.id == user_id))

        if not db_user:
            return False

        db_user.name = new_params.name
        self.session.commit()
        self.session.refresh(db_user)

        return db_user

    def verify_password(self, form_data) -> str:
        user = self.find_by_email(form_data.username)

        if not user or not verify_password(form_data.password, user.password):
            return False

        return str(user.id)

    def login_user(self, form_data, jti):
        now = datetime.now()

        user: User = self.find_by_email(form_data.username)

        user.jti = jti
        user.current_sign_in_at = now
        user.last_sign_in_at = now

        self.session.commit()
        self.session.refresh(user)

        return True

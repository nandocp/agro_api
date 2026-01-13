from sqlalchemy.orm import Session


class BaseRepository:
    def __init__(self, session=None):
        self.session: Session | None = session

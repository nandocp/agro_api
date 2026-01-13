import importlib
from abc import ABC
from typing import TypeVar

from sqlalchemy.orm import Session

from agro_api.entities.user import User

ModelType = TypeVar('ModelType')


def import_repository(model, session: Session):
    _package = 'agro_api.repositories'
    _klass = f'{model.__name__}Repository'

    try:
        module = importlib.import_module(_package)
        my_class = getattr(module, _klass)
        return my_class(model, session=session)
    except Exception as err:
        err.with_traceback()
        return None


class BaseService(ABC):
    def __init__(
        self,
        model: ModelType,
        session: None | Session = None,
        current_user: User | None = None,
    ) -> None:
        self.user = current_user
        self.repository = import_repository(model, session)

    async def get_many(self, filters):
        return await self.repository.get_many(filters)

    def extract_filters(filters):
        filters_dict = filters.dict()
        for key in ['offset', 'limit']:
            filters_dict.pop(key, None)

        items = filters_dict.items()
        return {key: val for key, val in items if val is not None}

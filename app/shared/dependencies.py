from typing import Annotated, Type, TypeVar

from fastapi import Depends, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.accounts.models import User
from config.authentication import get_current_user
from config.database import get_session

FilterSchemaType = TypeVar('FilterSchemaType', bound=BaseModel)

session = Annotated[AsyncSession, Depends(get_session)]
current_user = Annotated[User, Depends(get_current_user)]


def filters(filter_schema: Type[FilterSchemaType]):
    return Annotated[filter_schema, Query()]
